"""
Enterprise Recommendation Engine.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.recommendations.base import (
    BaseRecommendationEngine,
)

from app.recommendations.recommendation_result import (
    RecommendationDecision,
    RecommendationResult,
)

from app.risk.risk_result import RiskLevel

from app.duplicates.duplicate_result import DuplicateMatchType

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class InvoiceRecommendationEngine(
    BaseRecommendationEngine
):

    def recommend(
        self,
        context: AgentContext,
    ) -> RecommendationResult:

        # -----------------------------
        # Validation failed
        # -----------------------------

        if not context.is_valid:

            return RecommendationResult(

                decision=RecommendationDecision.REJECT,

                reason="Invoice validation failed.",

            )

        # -----------------------------
        # Blocked Vendor
        # -----------------------------

        if context.is_blocked_vendor:

            result = RecommendationResult(

                decision=RecommendationDecision.REJECT,

                reason="Vendor is blocked in the Vendor Database.",

            )

            result.add_action(
                "Reject invoice."
            )

            return result

        # -----------------------------
        # Exact Duplicate Invoice
        # -----------------------------

        if (
            context.duplicate_result is not None
            and context.duplicate_result.match_type == DuplicateMatchType.EXACT
        ):

            result = RecommendationResult(

                decision=RecommendationDecision.REJECT,

                reason="Exact duplicate invoice detected.",

            )

            result.add_action(
                "Reject invoice — duplicate detected."
            )

            return result

        # -----------------------------
        # Suspected Duplicate Invoice
        # -----------------------------

        if (
            context.duplicate_result is not None
            and context.duplicate_result.match_type == DuplicateMatchType.SUSPECTED
        ):

            result = RecommendationResult(

                decision=RecommendationDecision.MANAGER_REVIEW,

                reason="Suspected duplicate invoice.",

            )

            result.add_action(
                "Escalate to Manager for duplicate review."
            )

            return result

        # -----------------------------
        # Critical Risk
        # -----------------------------

        if context.risk_level == RiskLevel.CRITICAL:

            result = RecommendationResult(

                decision=RecommendationDecision.REJECT,

                reason="Critical business risk detected.",

            )

            result.add_action(
                "Reject invoice."
            )

            return result

        # -----------------------------
        # High Risk
        # -----------------------------

        if context.risk_level == RiskLevel.HIGH:

            result = RecommendationResult(

                decision=RecommendationDecision.MANAGER_REVIEW,

                reason="High-risk invoice.",

            )

            result.add_action(
                "Assign to Senior Finance Manager."
            )

            return result

        # -----------------------------
        # Medium Risk
        # -----------------------------

        if context.risk_level == RiskLevel.MEDIUM:

            result = RecommendationResult(

                decision=RecommendationDecision.FINANCE_REVIEW,

                reason="Requires finance review.",

            )

            result.add_action(
                "Queue for finance review."
            )

            return result

        # -----------------------------
        # Low Risk — passed every automated check
        # -----------------------------
        #
        # Even a "legal and safe" invoice — valid, no policy
        # violations, no duplicate suspicion, low risk score —
        # is deliberately NOT auto-approved. Automation only
        # flags problems here; the actual approve/reject call
        # always stays with a human. This keeps a person in the
        # loop on every invoice, not just the risky ones.

        result = RecommendationResult(

            decision=RecommendationDecision.FINANCE_REVIEW,

            reason=(
                "Invoice passed all automated checks — legal and "
                "low-risk, but still routed to a human for the "
                "final approve/reject decision rather than being "
                "auto-approved."
            ),

        )

        result.add_action(
            "Queue for finance sign-off (no automated approval)."
        )

        return result