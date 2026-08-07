"""
Vendor Record.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class VendorStatus(str, Enum):
    """
    Lifecycle status of a vendor inside the vendor database.
    """

    ACTIVE = "ACTIVE"

    BLOCKED = "BLOCKED"

    INACTIVE = "INACTIVE"


@dataclass
class Vendor:
    """
    Represents a single vendor tracked by the Vendor Database.
    """

    name: str

    normalized_key: str

    gst_number: str | None = None

    status: VendorStatus = VendorStatus.ACTIVE

    total_invoices: int = 0

    total_spend: float = 0.0

    currencies: set[str] = field(
        default_factory=set
    )

    first_seen: datetime = field(
        default_factory=datetime.utcnow
    )

    last_seen: datetime = field(
        default_factory=datetime.utcnow
    )

    # ---------------------------------------------------------

    def record_invoice(
        self,
        total_amount: float | None,
        currency: str | None,
        gst_number: str | None,
    ) -> None:
        """
        Update vendor statistics with a newly processed invoice.
        """

        self.total_invoices += 1

        if total_amount:

            self.total_spend += total_amount

        if currency:

            self.currencies.add(currency)

        if gst_number and not self.gst_number:

            self.gst_number = gst_number

        self.last_seen = datetime.utcnow()

    # ---------------------------------------------------------

    @property
    def is_blocked(self) -> bool:

        return self.status == VendorStatus.BLOCKED
