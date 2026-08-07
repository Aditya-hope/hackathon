"""
Base Audit Service.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.audit.audit_record import AuditRecord

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class BaseAuditService(ABC):

    @abstractmethod
    def create_record(
        self,
        context: AgentContext,
    ) -> AuditRecord:

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        record: AuditRecord,
    ) -> None:

        raise NotImplementedError