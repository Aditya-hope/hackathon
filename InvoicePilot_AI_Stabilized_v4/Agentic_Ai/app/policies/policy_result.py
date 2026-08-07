"""
Policy evaluation result.
"""

from dataclasses import dataclass, field
from enum import Enum


class PolicyDecision(str, Enum):
    """
    Final decision after policy evaluation.
    """

    APPROVED = "APPROVED"
    REVIEW = "REVIEW"
    REJECTED = "REJECTED"


@dataclass
class PolicyResult:
    """
    Result returned by the policy engine.
    """

    decision: PolicyDecision = PolicyDecision.APPROVED

    violations: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    # ---------------------------------------------------------

    def mark_for_review(self) -> None:
        """
        Mark this invoice for manual review.
        """

        if self.decision == PolicyDecision.APPROVED:
            self.decision = PolicyDecision.REVIEW

    # ---------------------------------------------------------

    def add_violation(
        self,
        message: str,
    ) -> None:

        self.decision = PolicyDecision.REJECTED

        self.violations.append(message)

    # ---------------------------------------------------------

    def add_recommendation(
        self,
        message: str,
    ) -> None:

        self.mark_for_review()

        self.recommendations.append(message)

    # ---------------------------------------------------------

    @property
    def approved(self) -> bool:

        return self.decision == PolicyDecision.APPROVED

    @property
    def requires_review(self) -> bool:

        return self.decision == PolicyDecision.REVIEW

    @property
    def rejected(self) -> bool:

        return self.decision == PolicyDecision.REJECTED