"""Portfolio Backend Application Package."""

import logging
import os

_log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(_log_dir, exist_ok=True)

_handler = logging.FileHandler(os.path.join(_log_dir, "app.log"))
_handler.setFormatter(logging.Formatter("%(asctime)s %(name)-30s %(levelname)s %(message)s"))

logger = logging.getLogger("app")
if not logger.handlers:
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
