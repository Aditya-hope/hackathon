"""
Unit tests for app.duplicates.duplicate_detector.DuplicateInvoiceDetector.
"""

from app.duplicates.duplicate_detector import DuplicateInvoiceDetector
from app.duplicates.duplicate_result import DuplicateMatchType
from app.schemas.invoice import Invoice


def _invoice(**overrides) -> Invoice:
    data = dict(
        vendor_name="Acme Supplies Pvt Ltd",
        invoice_number="INV-1001",
        invoice_date="2026-01-15",
        currency="INR",
        total_amount=12500.0,
    )
    data.update(overrides)
    return Invoice(**data)


def test_no_history_means_no_duplicate():
    detector = DuplicateInvoiceDetector()

    result = detector.check(_invoice(), execution_id="exec-1")

    assert not result.is_duplicate
    assert result.match_type == DuplicateMatchType.NONE


def test_exact_duplicate_same_vendor_and_invoice_number():
    detector = DuplicateInvoiceDetector()
    first = _invoice()
    detector.register(first, execution_id="exec-1")

    result = detector.check(_invoice(), execution_id="exec-2")

    assert result.is_duplicate
    assert result.match_type == DuplicateMatchType.EXACT
    assert "exec-1" in result.matched_execution_ids


def test_suspected_duplicate_same_amount_and_date_different_number():
    detector = DuplicateInvoiceDetector()
    first = _invoice(invoice_number="INV-1001")
    detector.register(first, execution_id="exec-1")

    resubmitted = _invoice(invoice_number="INV-9999")
    result = detector.check(resubmitted, execution_id="exec-2")

    assert result.is_duplicate
    assert result.match_type == DuplicateMatchType.SUSPECTED
    assert "exec-1" in result.matched_execution_ids


def test_different_vendor_is_never_a_duplicate():
    detector = DuplicateInvoiceDetector()
    detector.register(_invoice(), execution_id="exec-1")

    result = detector.check(
        _invoice(vendor_name="A Totally Different Vendor Ltd"),
        execution_id="exec-2",
    )

    assert not result.is_duplicate


def test_vendor_name_matching_is_case_and_whitespace_insensitive():
    detector = DuplicateInvoiceDetector()
    detector.register(_invoice(), execution_id="exec-1")

    result = detector.check(
        _invoice(vendor_name="  acme supplies pvt ltd  "),
        execution_id="exec-2",
    )

    assert result.is_duplicate
    assert result.match_type == DuplicateMatchType.EXACT
