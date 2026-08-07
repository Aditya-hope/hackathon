"""
Audit Service.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.audit.audit_record import AuditRecord
from app.audit.base import BaseAuditService

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class AuditService(BaseAuditService):

    def create_record(
        self,
        context: AgentContext,
    ) -> AuditRecord:

        timeline = [

            f"[{event.status}] "
            f"{event.skill}: {event.message}"

            for event in context.events

        ]

        return AuditRecord(

            execution_id=context.metadata.execution_id,

            invoice_number=(
                context.invoice.invoice_number
                if context.invoice
                else None
            ),

            vendor_name=(
                context.invoice.vendor_name
                if context.invoice
                else None
            ),

            recommendation=(
                str(context.recommendation)
                if context.recommendation
                else "NONE"
            ),

            risk_score=context.risk_score,

            provider=context.metadata.provider_used,

            processing_time=context.metadata.processing_time,

            timeline=timeline,

        )

    def save(
        self,
        record: AuditRecord,
    ) -> None:
        """
        Persist audit record.

        Version 1:
            Placeholder implementation.
        """

        print(record)