"""
Unit tests for app.policies.invoice_policy.InvoicePolicyEngine.
"""

from app.schemas.invoice import Invoice
from app.policies.invoice_policy import InvoicePolicyEngine
from app.policies.policy_result import PolicyDecision


def _invoice(**overrides) -> Invoice:
    data = dict(
        vendor_name="Acme Supplies Pvt Ltd",
        invoice_number="INV-1001",
        invoice_date="2026-01-15",
        currency="INR",
        total_amount=12500.0,
        purchase_order="PO-4471",
        gst_number="27ABCDE1234F1Z5",
    )
    data.update(overrides)
    return Invoice(**data)


def test_clean_invoice_is_approved():
    engine = InvoicePolicyEngine()

    result = engine.evaluate(_invoice())

    assert result.decision == PolicyDecision.APPROVED
    assert result.violations == []


def test_high_value_invoice_without_po_is_rejected():
    engine = InvoicePolicyEngine()

    result = engine.evaluate(
        _invoice(total_amount=75000.0, purchase_order=None)
    )

    assert result.decision == PolicyDecision.REJECTED
    assert any("Purchase Order" in v for v in result.violations)


def test_high_value_invoice_with_po_is_not_rejected_on_that_rule():
    engine = InvoicePolicyEngine()

    result = engine.evaluate(
        _invoice(total_amount=75000.0, purchase_order="PO-9001")
    )

    assert result.decision != PolicyDecision.REJECTED


def test_missing_gst_number_marks_for_review():
    engine = InvoicePolicyEngine()

    result = engine.evaluate(_invoice(gst_number=None))

    assert result.decision == PolicyDecision.REVIEW
    assert any("GST" in r for r in result.recommendations)


def test_foreign_currency_marks_for_review():
    engine = InvoicePolicyEngine()

    result = engine.evaluate(_invoice(currency="USD"))

    assert result.decision == PolicyDecision.REVIEW
    assert any("currency" in r.lower() for r in result.recommendations)


def test_violation_outranks_review_in_final_decision():
    # A rejection-triggering rule should never be downgraded back to
    # REVIEW by a later review-triggering rule.
    engine = InvoicePolicyEngine()

    result = engine.evaluate(
        _invoice(
            total_amount=75000.0,
            purchase_order=None,
            gst_number=None,
        )
    )

    assert result.decision == PolicyDecision.REJECTED
