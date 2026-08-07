"""
Base Skill Interface.

Every business skill must inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class BaseSkill(ABC):
    """
    Base class for all agent skills.
    """

    # ==========================================================
    # Skill Metadata
    # ==========================================================

    name: str = "base_skill"

    description: str = ""

    version: str = "1.0.0"

    author: str = "InvoicePilot AI"

    # ==========================================================
    # Execution
    # ==========================================================

    @abstractmethod
    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute the skill and return the updated context.
        """
        raise NotImplementedError

    # ==========================================================
    # Utility
    # ==========================================================

    def __str__(self) -> str:
        return f"{self.name} (v{self.version})"

    def __repr__(self) -> str:
        return self.__str__()