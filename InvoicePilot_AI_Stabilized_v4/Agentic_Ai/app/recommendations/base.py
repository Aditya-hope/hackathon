"""
Base Recommendation Engine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.recommendations.recommendation_result import (
    RecommendationResult,
)

if TYPE_CHECKING:
    from app.agent.context import AgentContext


class BaseRecommendationEngine(ABC):

    @abstractmethod
    def recommend(
        self,
        context: AgentContext,
    ) -> RecommendationResult:

        raise NotImplementedError