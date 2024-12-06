from datetime import datetime, timedelta
from elasticsearch import AsyncElasticsearch
from typing import Any
from dataclasses import dataclass
import pytz
from bs_monitoring.alert_services import alert, AlertService
from bs_monitoring.common.utils import ConfigField
from bs_monitoring.data_sources import DataSource, register_data_source


@dataclass
class ElasticDataSourceConfig:
    """Configuration for the Elasticsearch data source.

    Args:
        url (str): The URL for the Elasticsearch instance.
        indices (List[str]): The indices to consume messages from.
        basic_auth (Optional[List[str]], optional): Basic authentication credentials. Defaults to None.
        api_key (Optional[str], optional): API key for the Elasticsearch instance. Defaults to None.
        history_length (int, optional): The history length to consume messages from. Defaults to 1
    """

    url: str
    indices: list[str]
    basic_auth: list[str] | None = None
    api_key: str | None = None
    history_length: int = 1


@register_data_source
class ElasticDataSource(DataSource):
    basic_auth = ConfigField(list[str] | None, default=None)
    url = ConfigField(str)
    indices = ConfigField(list[str])
    api_key = ConfigField(str | None, default=None)
    history_length = ConfigField(int, default=1)

    def __init__(self, alert_service: AlertService, config: Any):
        """A data source that consumes messages from Elasticsearch.

        Args:
            args (ElasticDataSourceConfig): The configuration for the data source.
            alert_service (AlertService): The alert service to use.
        """
        super().__init__(config)
        auth = (
            {"basic_auth": tuple(self.basic_auth)}
            if self.basic_auth
            else {"api_key": self.api_key}
        )
        self.client_ = AsyncElasticsearch(self.url, **auth)
        self.indices = self.indices
        self.history_length_ = self.history_length
        self.alert_service = alert_service

        self.lookback = timedelta(days=self.history_length_)

    @alert(
        message="Failed to consume messages from Elasticsearch.",
    )
    async def produce(self) -> dict[str, list[dict[str, Any]]]:
        """Consumes messages from Elasticsearch since last check."""
        end = datetime.now(pytz.utc)
        start = end - self.lookback

        self.query_ = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": int(start.timestamp() * 1000),
                        "lte": int(end.timestamp() * 1000),
                    }
                }
            },
            "sort": [{"@timestamp": {"order": "desc"}}],
        }

        events = {}
        for index in self.indices:
            all_hits = []
            resp = await self.client_.search(
                index=index, body=self.query_, scroll="5m"
            )

            scroll_id = resp["_scroll_id"]
            hits = resp["hits"]["hits"]
            all_hits.extend(hit["_source"] for hit in hits)

            while len(hits) > 0:
                resp = await self.client_.scroll(scroll_id=scroll_id, scroll="5m")
                scroll_id = resp["_scroll_id"]
                hits = resp["hits"]["hits"]
                all_hits.extend(hit["_source"] for hit in hits)

            events[index] = all_hits

        return events

    async def close(self) -> None:
        """Clean up Elasticsearch client connection."""
        await self.client_.close()
