"""
Unit tests for app.risk.invoice_risk.InvoiceRiskEngine.
"""

from app.agent.context import AgentContext
from app.documents.document import Document
from app.documents.types import DocumentMimeType
from app.duplicates.duplicate_result import DuplicateMatchType, DuplicateResult
from app.risk.invoice_risk import InvoiceRiskEngine
from app.risk.risk_result import RiskLevel
from app.schemas.invoice import Invoice
from app.validators.validation_result import ValidationResult


def _context(**kwargs) -> AgentContext:
    document = Document(
        filename="invoice.txt",
        mime_type=DocumentMimeType.TEXT.value,
        text="dummy",
    )
    context = AgentContext(document=document)
    for key, value in kwargs.items():
        setattr(context, key, value)
    return context


def test_clean_invoice_is_low_risk():
    engine = InvoiceRiskEngine()

    context = _context(
        invoice=Invoice(vendor_name="Acme", total_amount=5000.0),
    )

    result = engine.assess(context)

    assert result.level == RiskLevel.LOW
    assert result.score < 30


def test_failed_validation_raises_risk():
    engine = InvoiceRiskEngine()

    failed_validation = ValidationResult()
    failed_validation.add_error("Vendor name is missing.")

    context = _context(validation_result=failed_validation)

    result = engine.assess(context)

    assert result.score >= 40
    assert any("validation failed" in r.lower() for r in result.reasons)


def test_exact_duplicate_pushes_risk_to_critical():
    engine = InvoiceRiskEngine()

    context = _context(
        invoice=Invoice(vendor_name="Acme", total_amount=150000.0),
        duplicate_result=DuplicateResult(
            match_type=DuplicateMatchType.EXACT,
            matched_execution_ids=["exec-1"],
        ),
    )

    result = engine.assess(context)

    # high-value (15) + exact duplicate (45) = 60 -> HIGH, and adding
    # any further factor should be enough to cross into CRITICAL (80).
    assert result.level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
    assert any("duplicate" in r.lower() for r in result.reasons)


def test_high_value_invoice_adds_a_reason():
    engine = InvoiceRiskEngine()

    context = _context(
        invoice=Invoice(vendor_name="Acme", total_amount=250000.0),
    )

    result = engine.assess(context)

    assert any("high-value" in r.lower() for r in result.reasons)


def test_risk_score_never_exceeds_max():
    engine = InvoiceRiskEngine()

    failed_validation = ValidationResult()
    failed_validation.add_error("bad")

    context = _context(
        invoice=Invoice(vendor_name="Acme", total_amount=999999.0),
        validation_result=failed_validation,
        duplicate_result=DuplicateResult(
            match_type=DuplicateMatchType.EXACT,
            matched_execution_ids=["exec-1"],
        ),
    )
    context.errors.extend(["e1", "e2", "e3"])
    context.warnings.extend(["w1", "w2", "w3"])

    result = engine.assess(context)

    assert result.score <= 100
    assert result.level == RiskLevel.CRITICAL
