"""
Duplicate Invoice Detection Result.
"""

from dataclasses import dataclass, field
from enum import Enum


class DuplicateMatchType(str, Enum):
    """
    Strength of a duplicate match.
    """

    NONE = "NONE"

    # Same vendor + same invoice number seen before.
    EXACT = "EXACT"

    # Same vendor + same amount + same invoice date,
    # but a different invoice number.
    SUSPECTED = "SUSPECTED"


@dataclass
class DuplicateResult:
    """
    Result returned by the Duplicate Invoice Detection engine.
    """

    match_type: DuplicateMatchType = DuplicateMatchType.NONE

    matched_execution_ids: list[str] = field(
        default_factory=list
    )

    reason: str = ""

    @property
    def is_duplicate(self) -> bool:

        return self.match_type != DuplicateMatchType.NONE
