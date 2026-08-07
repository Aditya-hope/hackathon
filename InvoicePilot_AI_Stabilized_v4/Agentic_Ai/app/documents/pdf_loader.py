"""
PDF document loader.
"""

from pathlib import Path

from app.documents.base import BaseDocumentLoader
from app.documents.document import Document
from app.documents.types import DocumentMimeType
from app.documents.exceptions import (
    DocumentLoadError,
    EmptyDocumentError,
    CorruptedPDFError,
)


class PDFLoader(BaseDocumentLoader):
    """
    Loads PDF documents and extracts their text.
    """

    name = "pdf"

    supported_extensions = [".pdf"]

    supported_mime_types = [DocumentMimeType.PDF.value]

    def load(self, file_path: str) -> Document:
        """
        Load a PDF document and extract text.
        """

        # Imported lazily so a missing PyMuPDF install only breaks
        # PDF loading, not the whole DocumentLoader (which always
        # instantiates every loader, including this one, up front).
        try:
            import pymupdf as fitz

        except ImportError as e:
            raise DocumentLoadError(
                "The 'pymupdf' package is not installed. "
                "Run: pip install pymupdf"
            ) from e

        try:
            pdf = fitz.open(file_path)

        except Exception as e:
            raise CorruptedPDFError(
                f"Unable to open PDF: {file_path}"
            ) from e

        try:
            text = "".join(page.get_text() for page in pdf)

            metadata = {
                "source": "pdf_loader",
                "pages": len(pdf),
            }

        finally:
            pdf.close()

        if not text.strip():
            raise EmptyDocumentError(
                "No readable text found in PDF."
            )

        return Document(
            filename=Path(file_path).name,
            mime_type=DocumentMimeType.PDF.value,
            text=text,
            metadata=metadata,
        )
