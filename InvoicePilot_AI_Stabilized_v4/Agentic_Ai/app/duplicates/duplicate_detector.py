"""
Enterprise Duplicate Invoice Detection Engine.

Version 1:
    In-memory implementation. Keeps a rolling history of every
    invoice processed so subsequent submissions can be compared
    against it. Swappable later for a real persistence layer since
    callers only depend on ``BaseDuplicateDetector``.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import TYPE_CHECKING

from app.duplicates.base import BaseDuplicateDetector
from app.duplicates.duplicate_result import (
    DuplicateMatchType,
    DuplicateResult,
)
from app.vendors.vendor_repository import normalize_vendor_name

if TYPE_CHECKING:
    from app.schemas.invoice import Invoice


@dataclass
class _InvoiceRecord:
    """
    Lightweight fingerprint of a previously processed invoice.
    """

    execution_id: str

    vendor_key: str

    invoice_number: str | None

    total_amount: float | None

    invoice_date: str | None


class DuplicateInvoiceDetector(BaseDuplicateDetector):
    """
    Detects duplicate (and suspected duplicate) invoice submissions.

    - EXACT: same vendor + same invoice number already processed.
    - SUSPECTED: same vendor + same amount + same invoice date, but
      a different (or missing) invoice number - e.g. a resubmission
      with a tampered invoice number.
    """

    def __init__(self):

        self._records: list[_InvoiceRecord] = []

        self._lock = Lock()

    # ---------------------------------------------------------

    def check(
        self,
        invoice: "Invoice",
        execution_id: str,
    ) -> DuplicateResult:

        if invoice is None:

            return DuplicateResult()

        vendor_key = normalize_vendor_name(
            invoice.vendor_name or ""
        )

        if not vendor_key:

            return DuplicateResult()

        # -------------------------------------------------
        # Exact match: same vendor + same invoice number
        # -------------------------------------------------

        if invoice.invoice_number:

            exact_matches = [

                record

                for record in self._records

                if (

                    record.vendor_key == vendor_key

                    and record.invoice_number == invoice.invoice_number

                )

            ]

            if exact_matches:

                return DuplicateResult(

                    match_type=DuplicateMatchType.EXACT,

                    matched_execution_ids=[

                        record.execution_id
                        for record in exact_matches

                    ],

                    reason=(
                        f"An invoice numbered "
                        f"'{invoice.invoice_number}' from "
                        f"'{invoice.vendor_name}' was already processed."
                    ),

                )

        # -------------------------------------------------
        # Suspected match: same vendor + amount + date,
        # different invoice number
        # -------------------------------------------------

        if invoice.total_amount and invoice.invoice_date:

            suspected_matches = [

                record

                for record in self._records

                if (

                    record.vendor_key == vendor_key

                    and record.total_amount == invoice.total_amount

                    and record.invoice_date == invoice.invoice_date

                    and record.invoice_number != invoice.invoice_number

                )

            ]

            if suspected_matches:

                return DuplicateResult(

                    match_type=DuplicateMatchType.SUSPECTED,

                    matched_execution_ids=[

                        record.execution_id
                        for record in suspected_matches

                    ],

                    reason=(
                        f"Another invoice from '{invoice.vendor_name}' "
                        f"for the same amount and date was already "
                        f"processed under a different invoice number."
                    ),

                )

        return DuplicateResult()

    # ---------------------------------------------------------

    def register(
        self,
        invoice: "Invoice",
        execution_id: str,
    ) -> None:

        if invoice is None:

            return

        vendor_key = normalize_vendor_name(
            invoice.vendor_name or ""
        )

        if not vendor_key:

            return

        with self._lock:

            self._records.append(

                _InvoiceRecord(

                    execution_id=execution_id,

                    vendor_key=vendor_key,

                    invoice_number=invoice.invoice_number,

                    total_amount=invoice.total_amount,

                    invoice_date=invoice.invoice_date,

                )

            )
