"""
API Routes.

Provides endpoints for:

- Health
- Upload Validation
- Invoice Processing
"""

from pathlib import Path
import tempfile
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from app.agent.context import AgentContext
from app.agent.execution_store import execution_store
from app.agent.invoice_agent import InvoiceAgent
from app.assistant.reasoning_copilot import ReasoningCopilot
from app.api.dependencies import (
    get_approval_queue,
    get_document_loader,
    get_invoice_agent,
    get_vendor_repository,
)
from app.api.dependencies import get_reasoning_copilot
from app.api.models import (
    ApprovalDecisionRequest,
    ApprovalItemResponse,
    ApprovalQueueListResponse,
    BatchInvoiceItemResult,
    BatchProcessInvoiceResponse,
    DeleteExecutionResponse,
    DuplicateSummary,
    HealthResponse,
    InvoiceSummary,
    ProcessInvoiceResponse,
    ProcessInvoiceTextRequest,
    UploadResponse,
    VendorListResponse,
    VendorSummary,
)
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatRequest,
    ChatResponse,
)
from app.approval.approval_item import ApprovalItem
from app.approval.approval_queue import ApprovalQueueService
from app.approval.exceptions import (
    ApprovalAlreadyDecidedError,
    ApprovalItemNotFoundError,
)

from app.core import (
    logger,
    settings,
    MAX_UPLOAD_SIZE_MB,
    MAX_BATCH_INVOICES,
    SUPPORTED_DOCUMENT_TYPES,
)

from app.documents import DocumentLoader
from app.documents.document import Document
from app.documents.types import DocumentMimeType

from app.vendors.vendor_record import Vendor
from app.vendors.vendor_repository import VendorRepository

router = APIRouter()

MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024


# ============================================================
# Helpers
# ============================================================


async def _persist_upload(file: UploadFile) -> Path:
    """
    Validate and persist an uploaded file temporarily.
    """

    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in SUPPORTED_DOCUMENT_TYPES:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{suffix}'. "
                f"Supported types: {', '.join(SUPPORTED_DOCUMENT_TYPES)}"
            ),
        )

    contents = await file.read()

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    if len(contents) > MAX_UPLOAD_SIZE_BYTES:

        raise HTTPException(
            status_code=413,
            detail=(
                f"Maximum upload size is "
                f"{MAX_UPLOAD_SIZE_MB} MB."
            ),
        )

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    )

    try:

        tmp.write(contents)

    finally:

        tmp.close()

    return Path(tmp.name)


def _build_invoice_summary(
    context: AgentContext,
) -> InvoiceSummary | None:

    if context.invoice is None:

        return None

    invoice = context.invoice

    return InvoiceSummary(

        vendor_name=invoice.vendor_name,

        invoice_number=invoice.invoice_number,

        invoice_date=invoice.invoice_date,

        total_amount=invoice.total_amount,

        currency=invoice.currency,

    )


def _build_vendor_summary(
    vendor: Vendor,
    is_new_vendor: bool = False,
) -> VendorSummary:

    return VendorSummary(

        name=vendor.name,

        gst_number=vendor.gst_number,

        status=vendor.status.value,

        total_invoices=vendor.total_invoices,

        total_spend=vendor.total_spend,

        currencies=sorted(vendor.currencies),

        is_new_vendor=is_new_vendor,

        first_seen=vendor.first_seen,

        last_seen=vendor.last_seen,

    )


def _build_duplicate_summary(
    context: AgentContext,
) -> DuplicateSummary | None:

    result = context.duplicate_result

    if result is None:

        return None

    return DuplicateSummary(

        is_duplicate=result.is_duplicate,

        match_type=result.match_type.value,

        matched_execution_ids=result.matched_execution_ids,

        reason=result.reason,

    )


def _build_approval_item_response(
    item: ApprovalItem,
) -> ApprovalItemResponse:

    return ApprovalItemResponse(

        execution_id=item.execution_id,

        invoice_number=item.invoice_number,

        vendor_name=item.vendor_name,

        total_amount=item.total_amount,

        currency=item.currency,

        recommendation=item.recommendation,

        risk_level=item.risk_level,

        risk_score=item.risk_score,

        reason=item.reason,

        status=item.status.value,

        created_at=item.created_at,

        decided_at=item.decided_at,

        decided_by=item.decided_by,

        decision_notes=item.decision_notes,

    )


# ============================================================
# Health
# ============================================================


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
)
def health():

    return HealthResponse(

        status="healthy",

        application=settings.APP_NAME,

        version=settings.APP_VERSION,

        providers_configured=settings.configured_providers(),

    )


# ============================================================
# Upload
# ============================================================


@router.post(
    "/upload",
    response_model=UploadResponse,
    tags=["Documents"],
)
async def upload_file(
    file: UploadFile = File(...),
    loader: DocumentLoader = Depends(get_document_loader),
):

    tmp_path = await _persist_upload(file)

    try:

        try:

            document = loader.load(str(tmp_path))

        except Exception as e:

            logger.exception("Document loading failed.")

            raise HTTPException(
                status_code=400,
                detail=f"Unable to load document: {e}",
            )

        size = (

            len(document.content)

            if document.content

            else len(document.text.encode())

        )

        return UploadResponse(

            filename=file.filename or document.filename,

            mime_type=document.mime_type,

            size_bytes=size,

        )

    finally:

        tmp_path.unlink(missing_ok=True)


# ============================================================
# Process Invoice
# ============================================================


def _run_agent_and_build_response(
    document,
    agent: InvoiceAgent,
    approval_queue: ApprovalQueueService,
) -> ProcessInvoiceResponse:
    """
    Run a loaded document through the Invoice Agent and build the
    API response. Shared by the file-upload and pasted-text entry
    points so both go through identical processing.
    """

    context = AgentContext(
        document=document,
    )

    try:

        context = agent.process(context)

    except Exception:

        logger.exception(
            "Invoice Agent crashed."
        )

        raise HTTPException(
            status_code=500,
            detail="Invoice processing failed.",
        )

    vendor_summary = None

    if context.vendor_result is not None:

        vendor_summary = _build_vendor_summary(

            context.vendor_result.vendor,

            is_new_vendor=context.vendor_result.is_new_vendor,

        )

    queued_item = approval_queue.get(
        context.metadata.execution_id
    )

    return ProcessInvoiceResponse(

        success=context.completed,

        status=context.state.value,

        invoice=_build_invoice_summary(context),

        vendor=vendor_summary,

        duplicate=_build_duplicate_summary(context),

        recommendation=(
            context.recommendation.value
            if context.recommendation
            else None
        ),

        risk_level=(
            context.risk_level.value
            if context.risk_level
            else None
        ),

        risk_score=context.risk_score,

        requires_human_review=context.requires_review,

        queued_for_approval=queued_item is not None,

        errors=context.errors,

        warnings=context.warnings,

        events=[
            {
                "skill": e.skill,
                "state": e.state,
                "status": e.status,
                "message": e.message,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in context.events
        ],

        metadata={

            "execution_id": context.metadata.execution_id,

            "provider_used": context.metadata.provider_used,

            "processing_time": context.metadata.processing_time,

            "retry_count": context.metadata.retry_count,

            "skill_timings": context.metadata.skill_timings,

        },

    )


@router.post(
    "/process-invoice",
    response_model=ProcessInvoiceResponse,
    tags=["Invoices"],
)
async def process_invoice(
    file: UploadFile = File(...),
    agent: InvoiceAgent = Depends(get_invoice_agent),
    loader: DocumentLoader = Depends(get_document_loader),
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):

    tmp_path = await _persist_upload(file)

    try:

        try:

            document = loader.load(str(tmp_path))

        except Exception as e:

            logger.exception("Failed loading uploaded document.")

            raise HTTPException(
                status_code=400,
                detail=f"Unable to read document: {e}",
            )

    finally:

        tmp_path.unlink(missing_ok=True)

    logger.info(
        f"Processing invoice: {file.filename}"
    )

    return _run_agent_and_build_response(
        document,
        agent,
        approval_queue,
    )


# ============================================================
# Process Invoices — batch (as many as the user wants to upload)
# ============================================================


@router.post(
    "/process-invoices",
    response_model=BatchProcessInvoiceResponse,
    tags=["Invoices"],
)
async def process_invoices(
    files: List[UploadFile] = File(...),
    agent: InvoiceAgent = Depends(get_invoice_agent),
    loader: DocumentLoader = Depends(get_document_loader),
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):
    """
    Process any number of invoice files in a single request.

    Each file runs through the same pipeline as
    ``/process-invoice``, independently of the others - one bad
    or unreadable file doesn't stop the rest of the batch. The
    response lists a per-file result so the caller can show
    exactly which invoices succeeded and which need attention.
    """

    if not files:

        raise HTTPException(
            status_code=400,
            detail="No files were uploaded.",
        )

    if len(files) > MAX_BATCH_INVOICES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Too many files in one batch. Maximum is "
                f"{MAX_BATCH_INVOICES} invoices per upload."
            ),
        )

    results: list[BatchInvoiceItemResult] = []

    for upload in files:

        filename = upload.filename or "unnamed-file"

        try:

            tmp_path = await _persist_upload(upload)

        except HTTPException as e:

            results.append(
                BatchInvoiceItemResult(
                    filename=filename,
                    success=False,
                    error=str(e.detail),
                )
            )

            continue

        try:

            try:

                document = loader.load(str(tmp_path))

            except Exception as e:

                logger.exception(
                    f"Failed loading uploaded document: {filename}"
                )

                results.append(
                    BatchInvoiceItemResult(
                        filename=filename,
                        success=False,
                        error=f"Unable to read document: {e}",
                    )
                )

                continue

        finally:

            tmp_path.unlink(missing_ok=True)

        logger.info(
            f"Processing invoice (batch): {filename}"
        )

        try:

            response = _run_agent_and_build_response(
                document,
                agent,
                approval_queue,
            )

            results.append(
                BatchInvoiceItemResult(
                    filename=filename,
                    success=True,
                    result=response,
                )
            )

        except HTTPException as e:

            results.append(
                BatchInvoiceItemResult(
                    filename=filename,
                    success=False,
                    error=str(e.detail),
                )
            )

    succeeded = sum(1 for r in results if r.success)

    return BatchProcessInvoiceResponse(
        count=len(results),
        succeeded=succeeded,
        failed=len(results) - succeeded,
        results=results,
    )


# ============================================================
# Process Invoice — pasted / typed text
# ============================================================


@router.post(
    "/process-invoice-text",
    response_model=ProcessInvoiceResponse,
    tags=["Invoices"],
)
async def process_invoice_text(
    request: ProcessInvoiceTextRequest,
    agent: InvoiceAgent = Depends(get_invoice_agent),
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):
    """
    Run raw invoice text — pasted or typed directly by the user,
    with no file involved — through the same agent pipeline used
    for uploaded documents, and return the same approval decision
    shape as ``/process-invoice``.
    """

    text = request.text.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Invoice text is empty.",
        )

    document = Document(
        filename=request.filename or "pasted-invoice.txt",
        mime_type=DocumentMimeType.TEXT.value,
        text=text,
        metadata={"source": "raw_text_input"},
    )

    logger.info(
        "Processing invoice from pasted/typed text "
        f"({len(text)} chars)."
    )

    return _run_agent_and_build_response(
        document,
        agent,
        approval_queue,
    )


# ============================================================
# Vendor Database
# ============================================================


@router.get(
    "/vendors",
    response_model=VendorListResponse,
    tags=["Vendors"],
)
def list_vendors(
    vendor_repository: VendorRepository = Depends(get_vendor_repository),
):

    vendors = [
        _build_vendor_summary(vendor)
        for vendor in vendor_repository.list_all()
    ]

    return VendorListResponse(
        vendors=vendors,
        count=len(vendors),
    )


@router.get(
    "/vendors/{vendor_name}",
    response_model=VendorSummary,
    tags=["Vendors"],
)
def get_vendor(
    vendor_name: str,
    vendor_repository: VendorRepository = Depends(get_vendor_repository),
):

    vendor = vendor_repository.get(vendor_name)

    if vendor is None:

        raise HTTPException(
            status_code=404,
            detail=f"No vendor found matching '{vendor_name}'.",
        )

    return _build_vendor_summary(vendor)


# ============================================================
# Approval Queue
# ============================================================


@router.get(
    "/approvals",
    response_model=ApprovalQueueListResponse,
    tags=["Approvals"],
)
def list_approvals(
    pending_only: bool = True,
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):
    """
    List entries in the Approval Queue.

    By default only PENDING entries are returned; pass
    ``pending_only=false`` to see the full history.
    """

    items = (
        approval_queue.list_pending()
        if pending_only
        else approval_queue.list_all()
    )

    responses = [
        _build_approval_item_response(item)
        for item in items
    ]

    return ApprovalQueueListResponse(
        items=responses,
        count=len(responses),
    )


@router.get(
    "/approvals/{execution_id}",
    response_model=ApprovalItemResponse,
    tags=["Approvals"],
)
def get_approval(
    execution_id: str,
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):

    item = approval_queue.get(execution_id)

    if item is None:

        raise HTTPException(
            status_code=404,
            detail=f"No approval queue entry for '{execution_id}'.",
        )

    return _build_approval_item_response(item)


@router.post(
    "/approvals/{execution_id}/approve",
    response_model=ApprovalItemResponse,
    tags=["Approvals"],
)
def approve_invoice(
    execution_id: str,
    decision: ApprovalDecisionRequest = ApprovalDecisionRequest(),
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):
    """
    Approve an invoice sitting in the Approval Queue.
    """

    try:

        item = approval_queue.approve(

            execution_id,

            decided_by=decision.decided_by,

            notes=decision.notes,

        )

    except ApprovalItemNotFoundError as e:

        raise HTTPException(status_code=404, detail=str(e))

    except ApprovalAlreadyDecidedError as e:

        raise HTTPException(status_code=409, detail=str(e))

    logger.info(
        f"Invoice approved: execution_id={execution_id} "
        f"by={decision.decided_by}"
    )

    return _build_approval_item_response(item)


@router.post(
    "/approvals/{execution_id}/reject",
    response_model=ApprovalItemResponse,
    tags=["Approvals"],
)
def reject_invoice(
    execution_id: str,
    decision: ApprovalDecisionRequest = ApprovalDecisionRequest(),
    approval_queue: ApprovalQueueService = Depends(get_approval_queue),
):
    """
    Reject an invoice sitting in the Approval Queue.
    """

    try:

        item = approval_queue.reject(

            execution_id,

            decided_by=decision.decided_by,

            notes=decision.notes,

        )

    except ApprovalItemNotFoundError as e:

        raise HTTPException(status_code=404, detail=str(e))

    except ApprovalAlreadyDecidedError as e:

        raise HTTPException(status_code=409, detail=str(e))

    logger.info(
        f"Invoice rejected: execution_id={execution_id} "
        f"by={decision.decided_by}"
    )

    return _build_approval_item_response(item)

# ============================================================
# AI Assistant
# ============================================================

@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["AI Assistant"],
)
def chat(
    request: ChatRequest,
    copilot: ReasoningCopilot = Depends(
        get_reasoning_copilot
    ),
):
    """
    AI Copilot endpoint.

    Allows users to ask natural language
    questions about a processed invoice.
    """

    return copilot.chat(

        execution_id=request.execution_id,

        question=request.question,

    )


@router.get(
    "/chat/{execution_id}/history",
    response_model=ChatHistoryResponse,
    tags=["AI Assistant"],
)
def get_chat_history(
    execution_id: str,
    copilot: ReasoningCopilot = Depends(
        get_reasoning_copilot
    ),
):
    """
    Return the saved conversation for an invoice execution.

    Lets the frontend restore a chat thread (e.g. after a page
    reload) instead of only relying on client-side state.
    """

    return ChatHistoryResponse(
        execution_id=execution_id,
        messages=copilot.get_history(execution_id),
    )


@router.delete(
    "/chat/{execution_id}/history",
    tags=["AI Assistant"],
)
def delete_chat_history(
    execution_id: str,
    copilot: ReasoningCopilot = Depends(
        get_reasoning_copilot
    ),
):
    """
    Permanently clear the saved conversation for an invoice
    execution.
    """

    copilot.clear_history(execution_id)

    return {"execution_id": execution_id, "cleared": True}


# ============================================================
# Executions (History tab "remove invoice")
# ============================================================


@router.delete(
    "/executions/{execution_id}",
    response_model=DeleteExecutionResponse,
    tags=["Invoices"],
)
def delete_execution(
    execution_id: str,
    copilot: ReasoningCopilot = Depends(
        get_reasoning_copilot
    ),
):
    """
    Remove an invoice the user has chosen to delete from their
    History tab.

    Clears the execution from the in-memory store, its persisted
    snapshot, and its AI Copilot chat history, so a removed invoice
    is genuinely gone rather than just hidden in the UI. This does
    not touch the Vendor Database or Approval Queue — those are
    separate audit trails, not view state.
    """

    execution_store.delete(execution_id)

    copilot.clear_history(execution_id)

    return DeleteExecutionResponse(
        execution_id=execution_id,
        deleted=True,
    )