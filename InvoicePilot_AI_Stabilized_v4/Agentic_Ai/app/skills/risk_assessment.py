"""
Risk Assessment Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.risk import RiskLevel
from app.risk.invoice_risk import InvoiceRiskEngine

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class RiskAssessmentSkill(BaseSkill):
    """
    Assess invoice risk based on the
    accumulated execution context.
    """

    name = "risk_assessment"

    description = (
        "Calculate the overall risk score "
        "for the invoice."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        risk_engine: InvoiceRiskEngine,
    ):

        self.risk_engine = risk_engine

    # ---------------------------------------------------------

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.RISK_ANALYSIS
        )

        result = self.risk_engine.assess(
            context
        )

        context.set_risk_result(
            result
        )

        if result.level == RiskLevel.LOW:

            status = "SUCCESS"

        elif result.level == RiskLevel.MEDIUM:

            status = "WARNING"

        elif result.level == RiskLevel.HIGH:

            status = "WARNING"

        else:

            status = "FAILED"

        context.add_event(

            skill=self.name,

            message=(
                f"Risk Score: {result.score:.1f} "
                f"({result.level.value})"
            ),

            status=status,

        )

        return context