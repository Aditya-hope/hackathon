"""
Document type definitions used throughout the document
processing module.
"""

from enum import Enum


class DocumentMimeType(str, Enum):
    """
    Supported document MIME types.

    This is the single source of truth for MIME types across the
    document processing module. Loaders, utilities, and the LLM
    layer all reference this enum instead of hardcoding MIME type
    strings.
    """

    PDF = "application/pdf"

    PNG = "image/png"

    # Both ".jpg" and ".jpeg" files map to this single MIME type —
    # "image/jpeg" is the standard/registered MIME type for both
    # extensions. ``JPG`` is kept as a name for backwards
    # compatibility; since it shares the same value as ``JPEG``,
    # Python treats it as an alias (DocumentMimeType.JPG is
    # DocumentMimeType.JPEG).
    JPEG = "image/jpeg"

    JPG = JPEG

    TEXT = "text/plain"


# Backwards-compatible alias. Some older modules referred to this
# type as ``DocumentType``; both names point at the same enum so
# any stray imports keep working while the codebase standardizes
# on ``DocumentMimeType``.
DocumentType = DocumentMimeType
