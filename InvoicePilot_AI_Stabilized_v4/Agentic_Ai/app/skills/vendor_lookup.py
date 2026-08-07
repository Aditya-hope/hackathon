"""
Vendor Lookup Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.skills.base import BaseSkill

from app.vendors.vendor_repository import VendorRepository

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class VendorLookupSkill(BaseSkill):
    """
    Look up the invoice's vendor in the Vendor Database,
    registering new vendors and updating running statistics
    (invoice count, total spend, currencies seen) for known ones.
    """

    name = "vendor_lookup"

    description = (
        "Look up the vendor in the Vendor Database and "
        "record invoice activity against it."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        vendor_repository: VendorRepository,
    ):

        self.vendor_repository = vendor_repository

    # ---------------------------------------------------------

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.VENDOR_LOOKUP
        )

        result = self.vendor_repository.record_invoice(
            context.invoice
        )

        context.set_vendor_result(
            result
        )

        if result.is_blocked:

            # Same reasoning as duplicate detection: this skill did its
            # job correctly by flagging the blocked vendor — it didn't
            # fail. Show it as a warning rather than FAILED so the
            # pipeline UI doesn't read the finding as a broken step.
            # The recommendation engine still rejects blocked-vendor
            # invoices outright, so this is a display change only.

            context.add_event(

                skill=self.name,

                message=result.reason,

                status="WARNING",

            )

        elif result.is_new_vendor:

            context.add_event(

                skill=self.name,

                message=result.reason,

                status="WARNING",

            )

        else:

            context.add_event(

                skill=self.name,

                message=result.reason,

                status="SUCCESS",

            )

        return context
