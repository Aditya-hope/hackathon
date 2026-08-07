"""
Approval Queue Item.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ApprovalStatus(str, Enum):
    """
    Lifecycle status of an item sitting in the Approval Queue.
    """

    PENDING = "PENDING"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"


@dataclass
class ApprovalItem:
    """
    A single invoice awaiting (or having received) a human
    approve/reject decision.
    """

    execution_id: str

    invoice_number: str | None

    vendor_name: str | None

    total_amount: float | None

    currency: str | None

    recommendation: str | None

    risk_level: str | None

    risk_score: float

    reason: str = ""

    status: ApprovalStatus = ApprovalStatus.PENDING

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    decided_at: datetime | None = None

    decided_by: str | None = None

    decision_notes: str | None = None

    # ---------------------------------------------------------

    def approve(
        self,
        decided_by: str | None = None,
        notes: str | None = None,
    ) -> None:

        self.status = ApprovalStatus.APPROVED

        self.decided_at = datetime.utcnow()

        self.decided_by = decided_by

        self.decision_notes = notes

    def reject(
        self,
        decided_by: str | None = None,
        notes: str | None = None,
    ) -> None:

        self.status = ApprovalStatus.REJECTED

        self.decided_at = datetime.utcnow()

        self.decided_by = decided_by

        self.decision_notes = notes

    @property
    def is_pending(self) -> bool:

        return self.status == ApprovalStatus.PENDING
