"""
Common document model used throughout InvoicePilot AI.

Every document loader must return a Document object.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Document:
    """
    Represents a normalized document after loading.
    """

    # Original filename
    filename: str

    # MIME type string, e.g. one of the values in DocumentMimeType
    mime_type: str

    # Extracted text
    text: str = ""

    # Images extracted from document (optional)
    images: List[Any] = field(default_factory=list)

    # Original file bytes (optional)
    content: Optional[bytes] = None

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)