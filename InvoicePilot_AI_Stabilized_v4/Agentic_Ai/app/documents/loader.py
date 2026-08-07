"""
Document Loader Factory.

Selects the appropriate loader for an uploaded document.
"""

from app.documents.base import BaseDocumentLoader
from app.documents.document import Document

from app.documents.pdf_loader import PDFLoader
from app.documents.image_loader import ImageLoader
from app.documents.text_loader import TextLoader

from app.documents.utils import get_extension

from app.documents.exceptions import (
    UnsupportedDocumentError,
)


class DocumentLoader:
    """
    Factory responsible for selecting the appropriate
    document loader.
    """

    def __init__(self):

        self.loaders: list[BaseDocumentLoader] = [
            PDFLoader(),
            ImageLoader(),
            TextLoader(),
        ]

    def load(self, file_path: str) -> Document:
        """
        Load a document using the first compatible loader.
        """

        extension = get_extension(file_path)

        for loader in self.loaders:

            if extension in loader.supported_extensions:
                return loader.load(file_path)

        raise UnsupportedDocumentError(
            f"Unsupported document type: {file_path}"
        )
