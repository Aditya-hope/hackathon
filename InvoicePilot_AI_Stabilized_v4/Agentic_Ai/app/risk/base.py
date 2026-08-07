"""
Base Risk Engine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.risk.risk_result import RiskResult

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class BaseRiskEngine(ABC):

    @abstractmethod
    def assess(
        self,
        context: AgentContext,
    ) -> RiskResult:
        raise NotImplementedError