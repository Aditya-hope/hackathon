"""
Audit Record.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditRecord:
    """
    Represents one completed invoice workflow.
    """

    execution_id: str

    invoice_number: str | None

    vendor_name: str | None

    recommendation: str

    risk_score: float

    provider: str | None

    processing_time: float | None

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    timeline: list[str] = field(
        default_factory=list
    )