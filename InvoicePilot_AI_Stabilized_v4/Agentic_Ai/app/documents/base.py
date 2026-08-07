"""
Base interface for all document loaders.
"""

from abc import ABC, abstractmethod

from app.documents.document import Document


class BaseDocumentLoader(ABC):
    """
    Base class for all document loaders.

    Every document loader must return a normalized
    Document object.
    """

    name: str = "base"

    supported_extensions: list[str] = []

    @abstractmethod
    def load(self, file_path: str) -> Document:
        """
        Load a document from disk and return a
        normalized Document object.
        """
        raise NotImplementedError