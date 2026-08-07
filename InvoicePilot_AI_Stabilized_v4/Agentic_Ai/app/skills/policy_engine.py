"""
Policy Engine Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.policies import (
    InvoicePolicyEngine,
    PolicyDecision,
)

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class PolicyEngineSkill(BaseSkill):

    name = "policy_engine"

    description = (
        "Evaluate invoice against enterprise policies."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        policy_engine: InvoicePolicyEngine,
    ):

        self.policy_engine = policy_engine

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.POLICY_CHECK
        )

        result = self.policy_engine.evaluate(
            context.invoice
        )

        context.set_policy_result(
            result
        )

        if result.decision == PolicyDecision.APPROVED:

            context.add_event(

                skill=self.name,

                message="Policy evaluation approved.",

                status="SUCCESS",

            )

        elif result.decision == PolicyDecision.REVIEW:

            context.add_event(

                skill=self.name,

                message="Policy requires human review.",

                status="WARNING",

            )

        else:

            # A policy violation (e.g. missing PO above threshold) is a
            # flag raised by a skill that ran successfully, not a
            # technical failure — same reasoning as duplicate detection
            # and vendor lookup above. Show it as a warning; the invoice
            # still goes to a human either way, since nothing in this
            # pipeline auto-approves.

            context.add_event(

                skill=self.name,

                message="Policy rejected the invoice — requires human review.",

                status="WARNING",

            )

        return context