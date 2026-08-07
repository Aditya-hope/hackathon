"""
Enterprise Vendor Database.

Version 1:
    In-memory implementation, keyed by a normalized vendor name.
    Swappable later for a real persistence layer (Postgres, etc.)
    since callers only depend on ``BaseVendorRepository``.
"""

from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING

from app.vendors.base import BaseVendorRepository
from app.vendors.vendor_record import Vendor, VendorStatus
from app.vendors.vendor_result import VendorLookupResult

if TYPE_CHECKING:
    from app.schemas.invoice import Invoice


def normalize_vendor_name(name: str) -> str:
    """
    Normalize a vendor name into a stable lookup key.
    """

    return " ".join(
        name.strip().lower().split()
    )


class VendorRepository(BaseVendorRepository):
    """
    Enterprise Vendor Database.

    Tracks every vendor seen by the system, along with running
    invoice/spend statistics, so downstream skills (policy, risk,
    recommendation) can reason about vendor history.
    """

    def __init__(self):

        self._vendors: dict[str, Vendor] = {}

        self._lock = Lock()

    # ---------------------------------------------------------
    # Reads
    # ---------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Vendor | None:

        if not name:

            return None

        return self._vendors.get(
            normalize_vendor_name(name)
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.get(name) is not None

    def list_all(
        self,
    ) -> list[Vendor]:

        return list(self._vendors.values())

    # ---------------------------------------------------------
    # Writes
    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        gst_number: str | None = None,
        status: VendorStatus = VendorStatus.ACTIVE,
    ) -> Vendor:
        """
        Manually register (or update) a vendor, independent of
        invoice processing. Useful for pre-seeding the database
        or for blocking a vendor.
        """

        key = normalize_vendor_name(name)

        with self._lock:

            vendor = self._vendors.get(key)

            if vendor is None:

                vendor = Vendor(
                    name=name,
                    normalized_key=key,
                    gst_number=gst_number,
                    status=status,
                )

                self._vendors[key] = vendor

            else:

                vendor.status = status

                if gst_number:

                    vendor.gst_number = gst_number

            return vendor

    def set_status(
        self,
        name: str,
        status: VendorStatus,
    ) -> Vendor | None:

        vendor = self.get(name)

        if vendor is None:

            return None

        vendor.status = status

        return vendor

    def record_invoice(
        self,
        invoice: "Invoice",
    ) -> VendorLookupResult:
        """
        Look up the invoice's vendor, creating a new vendor record
        on first sight, and update running statistics.
        """

        vendor_name = (invoice.vendor_name or "").strip()

        if not vendor_name:

            unknown = Vendor(
                name="UNKNOWN",
                normalized_key="",
            )

            return VendorLookupResult(
                vendor=unknown,
                is_new_vendor=True,
                reason="Invoice did not include a vendor name.",
            )

        key = normalize_vendor_name(vendor_name)

        with self._lock:

            vendor = self._vendors.get(key)

            is_new = vendor is None

            if is_new:

                vendor = Vendor(
                    name=vendor_name,
                    normalized_key=key,
                )

                self._vendors[key] = vendor

            vendor.record_invoice(
                total_amount=invoice.total_amount,
                currency=invoice.currency,
                gst_number=invoice.gst_number,
            )

        if vendor.is_blocked:

            return VendorLookupResult(
                vendor=vendor,
                is_new_vendor=is_new,
                is_blocked=True,
                reason=f"Vendor '{vendor.name}' is blocked.",
            )

        if is_new:

            return VendorLookupResult(
                vendor=vendor,
                is_new_vendor=True,
                reason=(
                    f"'{vendor.name}' is a new vendor "
                    f"with no prior invoice history."
                ),
            )

        return VendorLookupResult(
            vendor=vendor,
            is_new_vendor=False,
            reason=(
                f"'{vendor.name}' recognized "
                f"({vendor.total_invoices} invoice(s) on file)."
            ),
        )
