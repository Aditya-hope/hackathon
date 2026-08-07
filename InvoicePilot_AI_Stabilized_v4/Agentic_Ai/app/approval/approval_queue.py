"""
Enterprise Approval Queue.

Version 1:
    In-memory implementation, keyed by execution_id. Swappable
    later for a real persistence layer since callers only depend
    on ``BaseApprovalQueue``.
"""

from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING

from app.approval.approval_item import ApprovalItem, ApprovalStatus
from app.approval.base import BaseApprovalQueue
from app.approval.exceptions import (
    ApprovalAlreadyDecidedError,
    ApprovalItemNotFoundError,
)

from app.recommendations import RecommendationDecision

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class ApprovalQueueService(BaseApprovalQueue):
    """
    Holds invoices that require a human approve/reject decision.

    An invoice is queued whenever the workflow decides it cannot
    be auto-approved (policy review/rejection, or any final
    recommendation other than AUTO_APPROVE).
    """

    def __init__(self):

        self._items: dict[str, ApprovalItem] = {}

        self._lock = Lock()

    # ---------------------------------------------------------

    def enqueue(
        self,
        context: "AgentContext",
    ) -> ApprovalItem | None:
        """
        Add the current invoice to the approval queue if it needs
        a human decision. Returns None when no queue entry was
        necessary (e.g. the invoice was auto-approved).
        """

        if not self._requires_approval(context):

            return None

        invoice = context.invoice

        item = ApprovalItem(

            execution_id=context.metadata.execution_id,

            invoice_number=(
                invoice.invoice_number if invoice else None
            ),

            vendor_name=(
                invoice.vendor_name if invoice else None
            ),

            total_amount=(
                invoice.total_amount if invoice else None
            ),

            currency=(
                invoice.currency if invoice else None
            ),

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

            reason=(
                context.recommendation_result.reason
                if context.recommendation_result
                else "Requires manual review."
            ),

        )

        with self._lock:

            self._items[item.execution_id] = item

        return item

    @staticmethod
    def _requires_approval(
        context: "AgentContext",
    ) -> bool:

        if context.requires_review:

            return True

        if (

            context.recommendation is not None

            and context.recommendation != RecommendationDecision.AUTO_APPROVE

        ):

            return True

        return False

    # ---------------------------------------------------------

    def get(
        self,
        execution_id: str,
    ) -> ApprovalItem | None:

        return self._items.get(execution_id)

    def list_all(
        self,
    ) -> list[ApprovalItem]:

        return list(self._items.values())

    def list_pending(
        self,
    ) -> list[ApprovalItem]:

        return [

            item

            for item in self._items.values()

            if item.status == ApprovalStatus.PENDING

        ]

    # ---------------------------------------------------------

    def _get_or_raise(
        self,
        execution_id: str,
    ) -> ApprovalItem:

        item = self._items.get(execution_id)

        if item is None:

            raise ApprovalItemNotFoundError(
                f"No approval queue entry for execution_id "
                f"'{execution_id}'."
            )

        return item

    def approve(
        self,
        execution_id: str,
        decided_by: str | None = None,
        notes: str | None = None,
    ) -> ApprovalItem:

        with self._lock:

            item = self._get_or_raise(execution_id)

            if not item.is_pending:

                raise ApprovalAlreadyDecidedError(
                    f"Execution '{execution_id}' was already "
                    f"decided ({item.status.value})."
                )

            item.approve(
                decided_by=decided_by,
                notes=notes,
            )

            return item

    def reject(
        self,
        execution_id: str,
        decided_by: str | None = None,
        notes: str | None = None,
    ) -> ApprovalItem:

        with self._lock:

            item = self._get_or_raise(execution_id)

            if not item.is_pending:

                raise ApprovalAlreadyDecidedError(
                    f"Execution '{execution_id}' was already "
                    f"decided ({item.status.value})."
                )

            item.reject(
                decided_by=decided_by,
                notes=notes,
            )

            return item
