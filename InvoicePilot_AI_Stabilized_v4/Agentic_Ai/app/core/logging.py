"""
Application logging configuration.
"""

import logging

from app.core.config import settings


LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

logging.basicConfig(
    level=LOG_LEVEL,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("InvoicePilot")
logger.setLevel(LOG_LEVEL)
