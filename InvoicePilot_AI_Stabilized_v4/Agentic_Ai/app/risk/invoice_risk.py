"""
Enterprise Risk Assessment Engine.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.constants import (
    RISK_SCORE_VALIDATION_FAILED,
    RISK_SCORE_POLICY_REVIEW,
    RISK_SCORE_PER_ERROR,
    RISK_SCORE_PER_WARNING,
    RISK_SCORE_HIGH_VALUE_INVOICE,
    HIGH_VALUE_INVOICE_THRESHOLD,
    RISK_SCORE_DUPLICATE_SUSPECTED,
    RISK_SCORE_DUPLICATE_EXACT,
    RISK_SCORE_NEW_VENDOR,
    RISK_LEVEL_CRITICAL_THRESHOLD,
    RISK_LEVEL_HIGH_THRESHOLD,
    RISK_LEVEL_MEDIUM_THRESHOLD,
    RISK_SCORE_MAX,
)

from app.duplicates.duplicate_result import DuplicateMatchType

from app.risk.base import BaseRiskEngine

from app.risk.risk_result import (
    RiskLevel,
    RiskResult,
)

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class InvoiceRiskEngine(BaseRiskEngine):
    """
    Calculates the overall business risk
    for an invoice based on the execution context.
    """

    def assess(
        self,
        context: AgentContext,
    ) -> RiskResult:

        result = RiskResult()

        score = 0

        # =====================================================
        # Validation
        # =====================================================

        if not context.is_valid:

            score += RISK_SCORE_VALIDATION_FAILED

            result.add_reason(
                "Invoice validation failed."
            )

        # =====================================================
        # Policy
        # =====================================================

        if context.requires_review:

            score += RISK_SCORE_POLICY_REVIEW

            result.add_reason(
                "Policy review required."
            )

        # =====================================================
        # Errors
        # =====================================================

        if context.error_count:

            score += context.error_count * RISK_SCORE_PER_ERROR

            result.add_reason(
                f"{context.error_count} validation/policy error(s)."
            )

        # =====================================================
        # Warnings
        # =====================================================

        if context.warning_count:

            score += context.warning_count * RISK_SCORE_PER_WARNING

            result.add_reason(
                f"{context.warning_count} warning(s)."
            )

        # =====================================================
        # High Value Invoice
        # =====================================================

        if (
            context.invoice is not None
            and context.invoice.total_amount is not None
            and context.invoice.total_amount > HIGH_VALUE_INVOICE_THRESHOLD
        ):

            score += RISK_SCORE_HIGH_VALUE_INVOICE

            result.add_reason(
                "High-value invoice."
            )

        # =====================================================
        # Duplicate Invoice
        # =====================================================

        if (
            context.duplicate_result is not None
            and context.duplicate_result.match_type == DuplicateMatchType.EXACT
        ):

            score += RISK_SCORE_DUPLICATE_EXACT

            result.add_reason(
                "Exact duplicate invoice detected."
            )

        elif (
            context.duplicate_result is not None
            and context.duplicate_result.match_type == DuplicateMatchType.SUSPECTED
        ):

            score += RISK_SCORE_DUPLICATE_SUSPECTED

            result.add_reason(
                "Suspected duplicate invoice."
            )

        # =====================================================
        # New / Unrecognized Vendor
        # =====================================================

        if context.is_new_vendor:

            score += RISK_SCORE_NEW_VENDOR

            result.add_reason(
                "New vendor with no prior invoice history."
            )

        # =====================================================
        # Final Score
        # =====================================================

        score = min(score, RISK_SCORE_MAX)

        result.score = score

        # =====================================================
        # Risk Level
        # =====================================================

        if score >= RISK_LEVEL_CRITICAL_THRESHOLD:

            result.level = RiskLevel.CRITICAL

        elif score >= RISK_LEVEL_HIGH_THRESHOLD:

            result.level = RiskLevel.HIGH

        elif score >= RISK_LEVEL_MEDIUM_THRESHOLD:

            result.level = RiskLevel.MEDIUM

        else:

            result.level = RiskLevel.LOW

        return result