"""
Custom exceptions for the document processing module.
"""


class DocumentError(Exception):
    """
    Base exception for all document-related errors.
    """
    pass


class DocumentLoadError(DocumentError):
    """
    Raised when a document cannot be loaded.
    """
    pass


class UnsupportedDocumentError(DocumentError):
    """
    Raised when the uploaded document type is not supported.
    """
    pass


class EmptyDocumentError(DocumentError):
    """
    Raised when the document contains no readable content.
    """
    pass


class CorruptedPDFError(DocumentLoadError):
    """
    Raised when a PDF is corrupted or unreadable.
    """
    pass