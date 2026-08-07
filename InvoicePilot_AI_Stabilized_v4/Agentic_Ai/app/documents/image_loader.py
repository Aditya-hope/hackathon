"""
Image document loader.
"""

from pathlib import Path

from app.documents.base import BaseDocumentLoader
from app.documents.document import Document
from app.documents.types import DocumentMimeType
from app.documents.utils import detect_mime_type
from app.documents.exceptions import (
    EmptyDocumentError,
)


class ImageLoader(BaseDocumentLoader):
    """
    Loads image documents.

    Supported Formats:
    - PNG
    - JPG
    - JPEG
    """

    name = "image"

    supported_extensions = [
        ".png",
        ".jpg",
        ".jpeg",
    ]

    supported_mime_types = [
        DocumentMimeType.PNG.value,
        DocumentMimeType.JPEG.value,
    ]

    def load(self, file_path: str) -> Document:
        """
        Load an image document.
        """

        with open(file_path, "rb") as file:
            image_bytes = file.read()

        if not image_bytes:
            raise EmptyDocumentError(
                "Image file is empty."
            )

        mime_type = detect_mime_type(file_path)

        return Document(
            filename=Path(file_path).name,
            mime_type=mime_type.value,
            content=image_bytes,
            metadata={
                "source": "image_loader"
            },
        )
