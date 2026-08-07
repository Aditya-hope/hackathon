"""
Core package.

Provides centralized configuration,
logging, and shared constants.
"""

from .config import settings
from .logging import logger

from .constants import (
    SUPPORTED_DOCUMENT_TYPES,
    SUPPORTED_IMAGE_TYPES,
    SUPPORTED_PDF_TYPES,
    SUPPORTED_TEXT_TYPES,
    MAX_UPLOAD_SIZE_MB,
    MAX_BATCH_INVOICES,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_TEMPERATURE,
    REQUEST_TIMEOUT,
    MAX_PROVIDER_RETRIES,
    DEFAULT_LOG_LEVEL,
)

__all__ = [

    # Config
    "settings",

    # Logger
    "logger",

    # Document Constants
    "SUPPORTED_DOCUMENT_TYPES",
    "SUPPORTED_IMAGE_TYPES",
    "SUPPORTED_PDF_TYPES",
    "SUPPORTED_TEXT_TYPES",

    # Upload
    "MAX_UPLOAD_SIZE_MB",
    "MAX_BATCH_INVOICES",

    # AI
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DEFAULT_TEMPERATURE",
    "REQUEST_TIMEOUT",
    "MAX_PROVIDER_RETRIES",

    # Logging
    "DEFAULT_LOG_LEVEL",
]