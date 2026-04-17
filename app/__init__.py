"""Portfolio Backend Application Package."""

import logging
import os
import sys

logger = logging.getLogger("app")


def configure_logging() -> None:
    """Emit logs to stdout so platforms like Vercel can collect runtime logs."""
    root = logging.getLogger()
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    root.setLevel(getattr(logging, level_name, logging.INFO))

    if root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    )
    root.addHandler(handler)


configure_logging()
