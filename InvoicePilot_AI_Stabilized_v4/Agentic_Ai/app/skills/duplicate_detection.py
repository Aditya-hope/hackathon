"""
Duplicate Invoice Detection Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.duplicates.duplicate_detector import DuplicateInvoiceDetector
from app.duplicates.duplicate_result import DuplicateMatchType

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class DuplicateDetectionSkill(BaseSkill):
    """
    Check the extracted invoice against previously processed
    invoices to catch exact and suspected duplicate submissions.
    """

    name = "duplicate_detection"

    description = (
        "Detect duplicate or suspected duplicate "
        "invoice submissions."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        duplicate_detector: DuplicateInvoiceDetector,
    ):

        self.duplicate_detector = duplicate_detector

    # ---------------------------------------------------------

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.DUPLICATE_CHECK
        )

        result = self.duplicate_detector.check(
            context.invoice,
            context.metadata.execution_id,
        )

        context.set_duplicate_result(
            result
        )

        if result.match_type == DuplicateMatchType.EXACT:

            # A duplicate match is a flag for a human to review, not a
            # technical failure of this skill — the skill ran fine and
            # did exactly its job. Surface it as a warning, not FAILED,
            # so it doesn't read as a broken pipeline step. The invoice
            # itself still gets routed to REJECT by the recommendation
            # engine, so nothing gets auto-approved on the strength of
            # this softer status.

            context.add_event(

                skill=self.name,

                message=result.reason,

                status="WARNING",

            )

        elif result.match_type == DuplicateMatchType.SUSPECTED:

            context.add_event(

                skill=self.name,

                message=result.reason,

                status="WARNING",

            )

        else:

            context.add_event(

                skill=self.name,

                message="No duplicate invoice detected.",

                status="SUCCESS",

            )

        # Record this invoice so future submissions can be
        # compared against it, regardless of today's outcome.
        self.duplicate_detector.register(
            context.invoice,
            context.metadata.execution_id,
        )

        return context
