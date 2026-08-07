"""
Approval Queue Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.approval.approval_queue import ApprovalQueueService

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class ApprovalQueueSkill(BaseSkill):
    """
    Queue the invoice for a human approve/reject decision
    whenever it was not auto-approved by the workflow.
    """

    name = "approval_queue"

    description = (
        "Queue invoices that require a human "
        "approve/reject decision."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        approval_queue: ApprovalQueueService,
    ):

        self.approval_queue = approval_queue

    # ---------------------------------------------------------

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.QUEUEING_APPROVAL
        )

        item = self.approval_queue.enqueue(
            context
        )

        if item is not None:

            context.add_event(

                skill=self.name,

                message=(
                    f"Queued for approval "
                    f"(execution_id={item.execution_id})."
                ),

                status="WARNING",

            )

        else:

            context.add_event(

                skill=self.name,

                message="Auto-approved. No approval queue entry needed.",

                status="SUCCESS",

            )

        return context
