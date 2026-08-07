"""
Invoice Validation Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.skills.base import BaseSkill

from app.validators import InvoiceValidator

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class ValidateInvoiceSkill(BaseSkill):
    """
    Validate extracted invoice data.
    """

    name = "validate_invoice"

    description = (
        "Validate extracted invoice data "
        "using enterprise business rules."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        validator: InvoiceValidator,
    ):

        self.validator = validator

    # ---------------------------------------------------------

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.VALIDATING
        )

        result = self.validator.validate(
            context.invoice
        )

        # This already copies warnings and errors into the context.
        context.set_validation_result(
            result
        )

        # -----------------------------------------------------
        # Timeline Event
        # -----------------------------------------------------

        if result.valid:

            context.add_event(

                skill=self.name,

                message=(
                    f"Validation passed "
                    f"(Score: {result.score:.1f})"
                ),

                status="SUCCESS",

            )

        else:

            context.add_event(

                skill=self.name,

                message=(
                    f"Validation failed "
                    f"(Score: {result.score:.1f})"
                ),

                status="FAILED",

            )

        return context