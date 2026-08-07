"""
API request/response models.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    application: str
    version: str
    providers_configured: list[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    error: str
    detail: str


class UploadResponse(BaseModel):
    """
    Response returned by the standalone file upload endpoint.

    This only validates/stores the file - it does not run it
    through the agent. Use /process-invoice for that.
    """

    filename: str
    mime_type: str
    size_bytes: int


class ProcessInvoiceTextRequest(BaseModel):
    """
    Request body for submitting invoice text directly, without a
    file — e.g. pasted from an email or typed by the user.
    """

    text: str = Field(
        ...,
        min_length=1,
        description="Raw invoice text, pasted or typed by the user.",
    )

    filename: Optional[str] = Field(
        default=None,
        description="Optional display name for this text invoice.",
    )


class InvoiceSummary(BaseModel):
    """
    Slim, JSON-friendly view of the extracted invoice.
    """

    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None


class VendorSummary(BaseModel):
    """
    Slim, JSON-friendly view of a vendor from the Vendor Database.
    """

    name: str
    gst_number: Optional[str] = None
    status: str
    total_invoices: int
    total_spend: float
    currencies: list[str] = Field(default_factory=list)
    is_new_vendor: bool = False
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None


class DuplicateSummary(BaseModel):
    """
    Slim, JSON-friendly view of a duplicate detection result.
    """

    is_duplicate: bool
    match_type: str
    matched_execution_ids: list[str] = Field(default_factory=list)
    reason: str = ""


class ProcessInvoiceResponse(BaseModel):
    """
    Full result of running a document through the Invoice Agent.
    """

    success: bool

    status: str = Field(description="Final agent state, e.g. COMPLETED or FAILED")

    invoice: Optional[InvoiceSummary] = None

    vendor: Optional[VendorSummary] = None

    duplicate: Optional[DuplicateSummary] = None

    recommendation: Optional[str] = None

    risk_level: Optional[str] = None

    risk_score: float = 0.0

    requires_human_review: bool = False

    queued_for_approval: bool = False

    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)

    events: list[dict[str, Any]] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)


# ================================================================
# Batch Invoice Upload
# ================================================================


class BatchInvoiceItemResult(BaseModel):
    """
    Outcome for a single invoice within a batch upload.

    Each invoice in a batch is processed independently, so one
    failing file never prevents the others from completing.
    """

    filename: str

    success: bool

    result: Optional[ProcessInvoiceResponse] = None

    error: Optional[str] = None


class BatchProcessInvoiceResponse(BaseModel):
    """
    Result of running multiple documents through the Invoice Agent
    in a single request.
    """

    count: int = 0

    succeeded: int = 0

    failed: int = 0

    results: list[BatchInvoiceItemResult] = Field(default_factory=list)


# ================================================================
# Vendor Database
# ================================================================


class VendorListResponse(BaseModel):
    vendors: list[VendorSummary] = Field(default_factory=list)
    count: int = 0


# ================================================================
# Approval Queue
# ================================================================


class ApprovalItemResponse(BaseModel):
    """
    JSON-friendly view of an Approval Queue entry.
    """

    execution_id: str
    invoice_number: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    recommendation: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: float = 0.0
    reason: str = ""
    status: str
    created_at: datetime
    decided_at: Optional[datetime] = None
    decided_by: Optional[str] = None
    decision_notes: Optional[str] = None


class ApprovalQueueListResponse(BaseModel):
    items: list[ApprovalItemResponse] = Field(default_factory=list)
    count: int = 0


class ApprovalDecisionRequest(BaseModel):
    """
    Request body for the Approve / Reject APIs.
    """

    decided_by: Optional[str] = Field(
        default=None,
        description="Name/ID of the person making the decision.",
    )

    notes: Optional[str] = Field(
        default=None,
        description="Optional notes explaining the decision.",
    )


# ================================================================
# Execution deletion (History tab "remove invoice")
# ================================================================


class DeleteExecutionResponse(BaseModel):
    """
    Confirms an execution's stored data (in-memory context, the
    persisted snapshot, and its AI Copilot chat history) has been
    removed.
    """

    execution_id: str

    deleted: bool = True
