from bs_monitoring.monitors import create_monitors, Monitor
from bs_monitoring.alert_services import create_alert_service
from bs_monitoring.data_sources import create_data_source, DataSource
from bs_monitoring.databases import initialize_databases
from bs_monitoring.common.configs.base import RootConfig
import asyncio
import signal
from contextlib import AsyncExitStack


class Pipeline:
    def __init__(self, source: DataSource, monitors: list[Monitor], interval: int):
        self.source = source
        self.monitors = monitors
        self._exit_stack = AsyncExitStack()
        self._shutdown_event = asyncio.Event()
        self._interval = interval

    async def shutdown(self, signal=None):
        """Cleanup tasks tied to the service's shutdown."""

        self._shutdown_event.set()

        await self.source.close()

        for monitor in self.monitors:
            if hasattr(monitor, "close"):
                await monitor.close()

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    @staticmethod
    def construct(config: RootConfig):
        initialize_databases(config.Databases)

        alert_service = create_alert_service(config.AlertService)
        source = create_data_source(config.DataSource, alert_service)
        monitors = create_monitors(config.Monitors, alert_service)

        return Pipeline(source, monitors, config.Interval)

    async def _run(self):
        """Run the pipeline continuously using asyncio."""
        try:
            async for data in self.source.produce_continuous(self._interval):
                if self._shutdown_event.is_set():
                    break
                await asyncio.gather(
                    *[monitor.process(data) for monitor in self.monitors]
                )
        except asyncio.CancelledError:
            self._shutdown_event.set()
            return

    def run(self):
        """Entry point to run the pipeline in the event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Handle signals
        signals = (signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: asyncio.create_task(self.shutdown(signal=s))
            )

        try:
            loop.run_until_complete(self._run())
        except KeyboardInterrupt:
            loop.run_until_complete(self.shutdown())
        finally:
            tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
            if tasks:
                loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            loop.close()
