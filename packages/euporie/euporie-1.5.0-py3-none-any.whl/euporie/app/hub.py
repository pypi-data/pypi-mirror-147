"""Run euporie as a multi-client SSH server."""

import logging
from asyncio import get_event_loop
from typing import TYPE_CHECKING

from euporie.app.tui import TuiApp
from euporie.config import config
from euporie.log import setup_logs

if TYPE_CHECKING:
    from prompt_toolkit.contrib.ssh import PromptToolkitSSHSession

log = logging.getLogger(__name__)


class HubApp(TuiApp):
    """An app which runs as a multi-user SSH server."""

    @classmethod
    async def interact(cls, ssh_session: "PromptToolkitSSHSession") -> None:
        """Function to run the app asynchronously for the SSH server."""
        await cls().run_async()

    @classmethod
    def launch(cls) -> "None":
        """Launch the HubApp SSH server."""
        # Configure logging to include `asyncssh`'s log output
        setup_logs(
            {
                "handlers": {
                    "stdout": {
                        "share_stream": False,
                        "level": "DEBUG" if config.debug else "INFO",
                    }
                },
                "loggers": {
                    "asyncssh": {
                        "handlers": ["stdout"],
                        "level": "DEBUG" if config.debug else "INFO",
                    }
                },
            }
        )

        # Check we have asyncssh installed
        try:
            import asyncssh  # type: ignore
        except ModuleNotFoundError:
            log.critical(
                "Euporie hub requires the the `asyncssh` python package\n"
                'Install euporie hub with: "pip install euporie[hub]"'
            )
            import sys

            sys.exit(1)
        else:
            from prompt_toolkit.contrib.ssh import PromptToolkitSSHServer

        # Run the HubApp in an SSH server
        loop = get_event_loop()
        loop.run_until_complete(
            asyncssh.create_server(
                lambda: PromptToolkitSSHServer(interact=cls.interact),
                host=config.hub_ssh_host,
                port=config.hub_ssh_port,
                server_host_keys=config.hub_ssh_host_keys,
            )
        )
        log.info("Running euporie hub on port %s", config.hub_ssh_port)
        loop.run_forever()
