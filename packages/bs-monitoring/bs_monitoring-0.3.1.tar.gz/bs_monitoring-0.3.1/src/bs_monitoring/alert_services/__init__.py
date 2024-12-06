from __future__ import annotations
from bs_monitoring.alert_services.base import (
    AlertService,
    alert,
    create_alert_service,
    register_alert_service,
    AlertServiceConfig,
)

from bs_monitoring.alert_services.opsgenie import OpsgenieAlertService
from bs_monitoring.alert_services.discord import DiscordAlertService

__all__ = [
    "AlertService",
    "AlertServiceConfig",
    "alert",
    "create_alert_service",
    "register_alert_service",
]
