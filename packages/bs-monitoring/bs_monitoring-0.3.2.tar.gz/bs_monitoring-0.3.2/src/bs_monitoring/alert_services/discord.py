from typing import Any
import requests
from bs_monitoring.alert_services.base import AlertService, register_alert_service
from bs_monitoring.common.utils import ConfigField


@register_alert_service
class DiscordAlertService(AlertService):
    webhook_url = ConfigField(str)

    def __init__(self, config: Any):
        """Alert service that sends alerts to Discord via webhooks.
        
        To get the webhook URL:
        1. Go to Discord Server Settings
        2. Select "Integrations"
        3. Click on "Webhooks"
        4. Create a new webhook or use existing one
        5. Copy the Webhook URL

        Args:
            config: The configuration containing the webhook_url.
        """
        super().__init__(config)

    def build_alert(
        self,
        message: str,
        description: str | None = None,
        alias: str | None = None,
    ) -> dict[str, Any]:
        """Builds a Discord webhook message.

        Args:
            message (str): The message title for the alert.
            description (Optional[str]): Description for the alert. Defaults to None.
            alias (Optional[str]): Not used for Discord. Defaults to None.

        Returns:
            Dict[str, Any]: The Discord webhook message object.
        """
        embed = {
            "title": message,
            "description": description if description else message,
            "color": 15158332  # Red color for alerts
        }
        
        return {
            "embeds": [embed]
        }

    def send_alert(
        self,
        message: str,
        description: str | None = None,
    ):
        """Sends an alert to Discord via webhook.

        Args:
            message (str): Alert message
            description (Optional[str]): Alert description. Defaults to None.

        Raises:
            Exception: Raised if the alert could not be sent.
        """
        body = self.build_alert(message, description)
        
        response = requests.post(url=self.webhook_url, json=body)
        if response.status_code not in (200, 204):
            raise Exception(f"Failed to send alert to Discord: {response.text}") 
