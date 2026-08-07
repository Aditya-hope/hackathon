"""
FastAPI dependencies.
"""

from functools import lru_cache

from app.bootstrap import get_application
from app.assistant.reasoning_copilot import ReasoningCopilot
from app.agent.invoice_agent import InvoiceAgent
from app.agent.execution_store import execution_store
from app.documents import DocumentLoader
from app.vendors.vendor_repository import VendorRepository
from app.duplicates.duplicate_detector import DuplicateInvoiceDetector
from app.approval.approval_queue import ApprovalQueueService


@lru_cache
def get_invoice_agent() -> InvoiceAgent:
    """
    Return the singleton Invoice Agent.
    """

    application = get_application()

    return application.agent


@lru_cache
def get_document_loader() -> DocumentLoader:
    """
    Return a shared DocumentLoader instance.

    DocumentLoader is stateless, so a single shared instance is
    safe to reuse across requests.
    """

    return DocumentLoader()


@lru_cache
def get_vendor_repository() -> VendorRepository:
    """
    Return the singleton Vendor Database.
    """

    application = get_application()

    return application.vendor_repository


@lru_cache
def get_duplicate_detector() -> DuplicateInvoiceDetector:
    """
    Return the singleton Duplicate Invoice Detector.
    """

    application = get_application()

    return application.duplicate_detector


@lru_cache
def get_approval_queue() -> ApprovalQueueService:
    """
    Return the singleton Approval Queue.
    """

    application = get_application()

    return application.approval_queue

@lru_cache
def get_reasoning_copilot() -> ReasoningCopilot:
    """
    Return the singleton AI Copilot.
    """

    application = get_application()

    return application.reasoning_copilot


