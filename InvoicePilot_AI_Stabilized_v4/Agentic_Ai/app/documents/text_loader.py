"""
Plain text document loader.
"""

from pathlib import Path

from app.documents.base import BaseDocumentLoader
from app.documents.document import Document
from app.documents.types import DocumentMimeType
from app.documents.exceptions import EmptyDocumentError


class TextLoader(BaseDocumentLoader):
    """
    Loads plain text documents.
    """

    name = "text"

    supported_extensions = [
        ".txt",
    ]

    supported_mime_types = [DocumentMimeType.TEXT.value]

    def load(self, file_path: str) -> Document:
        """
        Load a text document.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            text = file.read()

        if not text.strip():
            raise EmptyDocumentError(
                "Text document is empty."
            )

        return Document(
            filename=Path(file_path).name,
            mime_type=DocumentMimeType.TEXT.value,
            text=text,
            metadata={
                "source": "text_loader"
            },
        )
