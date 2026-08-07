"""
Utility functions for document processing.

Centralizes MIME type detection so no loader has to duplicate
this logic.
"""

from pathlib import Path
import mimetypes

from app.documents.types import DocumentMimeType
from app.documents.exceptions import (
    UnsupportedDocumentError,
)


SUPPORTED_MIME_TYPES = {
    DocumentMimeType.PDF,
    DocumentMimeType.PNG,
    DocumentMimeType.JPEG,
    DocumentMimeType.TEXT,
}

# Extension -> MIME type, used as a fast/reliable fallback when the
# stdlib ``mimetypes`` module doesn't recognize an extension (or
# returns an unexpected value, e.g. some platforms map ".jpg" to
# "image/jpeg" while others don't).
#
# Both ".jpg" and ".jpeg" map to DocumentMimeType.JPEG — that's the
# single standard MIME type for both extensions.
EXTENSION_MIME_MAP: dict[str, DocumentMimeType] = {
    ".pdf": DocumentMimeType.PDF,
    ".png": DocumentMimeType.PNG,
    ".jpg": DocumentMimeType.JPEG,
    ".jpeg": DocumentMimeType.JPEG,
    ".txt": DocumentMimeType.TEXT,
}


def get_extension(file_path: str) -> str:
    """
    Return the lowercase file extension, including the leading dot.
    """

    return Path(file_path).suffix.lower()


def detect_mime_type(file_path: str) -> DocumentMimeType:
    """
    Detect the MIME type of a file.

    Tries the file extension map first (deterministic and covers
    every type this application supports), then falls back to the
    stdlib ``mimetypes`` guesser for anything else.
    """

    extension = get_extension(file_path)

    if extension in EXTENSION_MIME_MAP:
        return EXTENSION_MIME_MAP[extension]

    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        raise UnsupportedDocumentError(
            f"Unable to determine MIME type for '{file_path}'."
        )

    try:
        return DocumentMimeType(mime_type)

    except ValueError:
        raise UnsupportedDocumentError(
            f"Unsupported MIME type: {mime_type}"
        )


def is_pdf(file_path: str) -> bool:
    """
    Check whether the file is a PDF.
    """

    return detect_mime_type(file_path) == DocumentMimeType.PDF


def is_image(file_path: str) -> bool:
    """
    Check whether the file is an image.
    """

    return detect_mime_type(file_path) in {
        DocumentMimeType.PNG,
        DocumentMimeType.JPEG,
    }


def is_text(file_path: str) -> bool:
    """
    Check whether the file is a plain text file.
    """

    return detect_mime_type(file_path) == DocumentMimeType.TEXT


def validate_file(file_path: str) -> None:
    """
    Validate whether the file type is supported.
    """

    mime_type = detect_mime_type(file_path)

    if mime_type not in SUPPORTED_MIME_TYPES:
        raise UnsupportedDocumentError(
            f"{mime_type} is not supported."
        )
