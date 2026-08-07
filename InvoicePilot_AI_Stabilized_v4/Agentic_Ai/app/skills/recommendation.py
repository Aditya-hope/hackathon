"""
Recommendation Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.recommendations import RecommendationDecision
from app.recommendations.invoice_recommendation import (
    InvoiceRecommendationEngine,
)

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class RecommendationSkill(BaseSkill):
    """
    Generate the final business recommendation
    for the processed invoice.
    """

    name = "recommendation"

    description = (
        "Generate the final recommendation "
        "based on validation, policy and risk."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        recommendation_engine: InvoiceRecommendationEngine,
    ):

        self.recommendation_engine = recommendation_engine

    # ---------------------------------------------------------

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.RECOMMENDING
        )

        result = self.recommendation_engine.recommend(
            context
        )

        context.set_recommendation_result(
            result
        )

        # -----------------------------------------------------
        # Timeline Event
        # -----------------------------------------------------

        if result.decision == RecommendationDecision.AUTO_APPROVE:

            status = "SUCCESS"

        elif result.decision == RecommendationDecision.FINANCE_REVIEW:

            status = "WARNING"

        elif result.decision == RecommendationDecision.MANAGER_REVIEW:

            status = "WARNING"

        else:

            status = "FAILED"

        context.add_event(

            skill=self.name,

            message=result.reason,

            status=status,

        )

        return context