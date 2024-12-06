from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, AsyncGenerator
import asyncio
from datetime import datetime

from bs_monitoring.alert_services import AlertService
from bs_monitoring.common.utils import register_config


@dataclass
class DataSourceConfig:
    """Configuration for the data source component

    Args:
        type (str): The type of the data source.
        config (Union[ElasticDataSourceConfig, None], optional): The configuration for the data source. Defaults to None.
    """

    type: str
    config: None = None


class DataSource(ABC):
    def __init__(self, config: Any) -> None:
        for k, v in asdict(config).items():
            setattr(self, k, v)
        self.last_run = None

    @abstractmethod
    async def produce(self) -> dict[str, list[dict[str, Any]]]:
        """Single production of data from the data source."""
        pass

    async def produce_continuous(self, interval_seconds: int = 86400) -> AsyncGenerator[dict[str, list[dict[str, Any]]], None]:
        """Continuously produce data at specified intervals using asyncio.
        
        Args:
            interval_seconds (float): Interval between productions in seconds. Defaults to 86400 (1 day).
        """
        while True:
            current_time = datetime.now()
            
            if self.last_run is None or (current_time - self.last_run).total_seconds() >= interval_seconds:
                self.last_run = current_time
                yield await self.produce()
            
            await asyncio.sleep(interval_seconds)

    async def close(self) -> None:
        """Clean up any resources."""
        pass


def register_data_source(cls):
    assert issubclass(
        cls, DataSource
    ), f"Class {cls.__name__} must be a subclass of DataSource to be registered as one."

    name = (
        cls.__name__
        if not cls.__name__.endswith("DataSource")
        else cls.__name__.removesuffix("DataSource")
    )
    __DATA_SOURCES[name] = cls
    register_config(cls, DataSourceConfig)
    return cls


__DATA_SOURCES = {}


def create_data_source(
    config: DataSourceConfig, alert_service: AlertService
) -> DataSource:
    """Create a data source based on the configuration.

    Args:
        config (DataSourceConfig): The configuration for the data source.
        alert_service (AlertService): The alert service to use.

    Raises:
        Exception: If the data source type is unknown.

    Returns:
        DataSource: The data source subclass instance.
    """
    c = config.config if hasattr(config, "config") else None

    src = __DATA_SOURCES.get(config.type)
    if src is not None:
        return src(alert_service, c)
    else:
        raise Exception(f"Unknown data source type: {config.type}")
