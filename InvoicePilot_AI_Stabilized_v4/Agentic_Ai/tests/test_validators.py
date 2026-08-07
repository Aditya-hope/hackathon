"""
Unit tests for app.validators.invoice_validator.InvoiceValidator.

Pure business logic, no LLM / network calls involved.
"""

from app.schemas.invoice import Invoice
from app.validators.invoice_validator import InvoiceValidator


def _valid_invoice(**overrides) -> Invoice:
    data = dict(
        vendor_name="Acme Supplies Pvt Ltd",
        invoice_number="INV-1001",
        invoice_date="2026-01-15",
        currency="INR",
        total_amount=12500.0,
        purchase_order="PO-4471",
    )
    data.update(overrides)
    return Invoice(**data)


def test_valid_invoice_passes_with_no_errors():
    validator = InvoiceValidator()

    result = validator.validate(_valid_invoice())

    assert result.valid is True
    assert result.errors == []


def test_missing_vendor_name_is_an_error():
    validator = InvoiceValidator()

    result = validator.validate(_valid_invoice(vendor_name=None))

    assert result.valid is False
    assert any("Vendor name" in e for e in result.errors)


def test_missing_invoice_number_is_an_error():
    validator = InvoiceValidator()

    result = validator.validate(_valid_invoice(invoice_number=None))

    assert result.valid is False
    assert any("Invoice number" in e for e in result.errors)


def test_missing_invoice_date_is_an_error():
    validator = InvoiceValidator()

    result = validator.validate(_valid_invoice(invoice_date=None))

    assert result.valid is False
    assert any("date" in e.lower() for e in result.errors)


def test_zero_total_amount_is_an_error():
    validator = InvoiceValidator()

    result = validator.validate(_valid_invoice(total_amount=0))

    assert result.valid is False
    assert any("total amount" in e.lower() for e in result.errors)


def test_missing_purchase_order_is_only_a_warning():
    validator = InvoiceValidator()

    result = validator.validate(_valid_invoice(purchase_order=None))

    # A missing PO should not block the invoice on its own -
    # that's the policy engine's job (PO required above a threshold).
    assert result.valid is True
    assert any("purchase order" in w.lower() for w in result.warnings)


def test_score_drops_for_each_error_and_warning():
    validator = InvoiceValidator()

    result = validator.validate(
        _valid_invoice(vendor_name=None, purchase_order=None)
    )

    # base 100, -15 for the vendor error, -5 for the PO warning
    assert result.score == 100.0 - 15 - 5
