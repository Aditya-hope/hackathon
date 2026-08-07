"""
Risk Result.
"""

from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


@dataclass
class RiskResult:

    score: float = 0.0

    level: RiskLevel = RiskLevel.LOW

    reasons: list[str] = field(default_factory=list)

    def add_reason(
        self,
        message: str,
    ) -> None:

        self.reasons.append(message)