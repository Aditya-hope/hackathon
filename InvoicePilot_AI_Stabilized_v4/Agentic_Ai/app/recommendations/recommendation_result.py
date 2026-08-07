"""
Recommendation Result.
"""

from dataclasses import dataclass, field
from enum import Enum


class RecommendationDecision(str, Enum):
    """
    Final business decision.
    """

    AUTO_APPROVE = "AUTO_APPROVE"

    FINANCE_REVIEW = "FINANCE_REVIEW"

    MANAGER_REVIEW = "MANAGER_REVIEW"

    REJECT = "REJECT"


@dataclass
class RecommendationResult:
    """
    Final recommendation produced
    by the recommendation engine.
    """

    decision: RecommendationDecision

    reason: str

    actions: list[str] = field(
        default_factory=list
    )

    def add_action(
        self,
        action: str,
    ) -> None:

        self.actions.append(action)