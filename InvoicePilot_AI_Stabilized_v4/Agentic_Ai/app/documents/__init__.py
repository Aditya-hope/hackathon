"""
Document Processing Package.

This package provides document ingestion and normalization
for the InvoicePilot AI system.

Supported document types:
- PDF
- Images (PNG, JPG, JPEG)
- Plain Text

All document loaders return a common Document object.
"""

from .document import Document
from .base import BaseDocumentLoader
from .loader import DocumentLoader

from .pdf_loader import PDFLoader
from .image_loader import ImageLoader
from .text_loader import TextLoader

from .types import DocumentMimeType

from .utils import (
    detect_mime_type,
    get_extension,
    is_pdf,
    is_image,
    is_text,
    validate_file,
)

from .exceptions import (
    DocumentError,
    DocumentLoadError,
    UnsupportedDocumentError,
    EmptyDocumentError,
    CorruptedPDFError,
)

__all__ = [
    "Document",
    "BaseDocumentLoader",
    "DocumentLoader",
    "PDFLoader",
    "ImageLoader",
    "TextLoader",
    "DocumentMimeType",
    "detect_mime_type",
    "get_extension",
    "is_pdf",
    "is_image",
    "is_text",
    "validate_file",
    "DocumentError",
    "DocumentLoadError",
    "UnsupportedDocumentError",
    "EmptyDocumentError",
    "CorruptedPDFError",
]
