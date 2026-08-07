"""
Audit Logger Skill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agent.state import AgentState

from app.audit import (
    AuditLogger,
    AuditService,
)

from app.skills.base import BaseSkill

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class AuditLoggerSkill(BaseSkill):

    name = "audit_logger"

    description = (
        "Create and persist an audit record."
    )

    version = "1.0.0"

    author = "InvoicePilot AI"

    def __init__(
        self,
        audit_service: AuditService,
        audit_logger: AuditLogger,
    ):

        self.audit_service = audit_service
        self.audit_logger = audit_logger

    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:

        context.set_state(
            AgentState.AUDITING
        )

        record = self.audit_service.create_record(
            context
        )

        self.audit_service.save(record)

        self.audit_logger.log(record)

        context.add_event(
            skill=self.name,
            message="Audit record created.",
            status="SUCCESS",
        )

        return context