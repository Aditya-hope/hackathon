"""
Invoice Extraction Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.schemas.invoice import Invoice

from app.services.llm.llm_service import LLMService

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class ExtractInvoiceSkill(BaseSkill):

    name = "extract_invoice"

    description = (
        "Extract structured invoice data."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm = llm_service

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.EXTRACTING
        )

        invoice, provider, model = (
            self.llm.extract_invoice(
                context.document
            )
        )

        context.set_invoice(
            invoice
        )

        context.set_provider(
            provider=provider,
            model=model,
        )

        context.add_event(

            skill=self.name,

            message=(
                f"Invoice extracted successfully "
                f"using {provider}."
            )

        )

        return context