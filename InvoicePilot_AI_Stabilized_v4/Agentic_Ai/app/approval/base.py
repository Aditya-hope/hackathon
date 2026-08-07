"""
Base Approval Queue.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.approval.approval_item import ApprovalItem

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class BaseApprovalQueue(ABC):
    """
    Storage contract for the Approval Queue.
    """

    @abstractmethod
    def enqueue(
        self,
        context: "AgentContext",
    ) -> ApprovalItem | None:

        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        execution_id: str,
    ) -> ApprovalItem | None:

        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[ApprovalItem]:

        raise NotImplementedError

    @abstractmethod
    def list_pending(
        self,
    ) -> list[ApprovalItem]:

        raise NotImplementedError

    @abstractmethod
    def approve(
        self,
        execution_id: str,
        decided_by: str | None = None,
        notes: str | None = None,
    ) -> ApprovalItem:

        raise NotImplementedError

    @abstractmethod
    def reject(
        self,
        execution_id: str,
        decided_by: str | None = None,
        notes: str | None = None,
    ) -> ApprovalItem:

        raise NotImplementedError
