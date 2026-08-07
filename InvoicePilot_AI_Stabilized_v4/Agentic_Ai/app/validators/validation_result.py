"""
Validation Result.
"""

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """
    Result returned by invoice validation.
    """

    valid: bool = True

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    score: float = 100.0

    def add_error(
        self,
        message: str,
    ):

        self.valid = False

        self.errors.append(message)

        self.score -= 15

    def add_warning(
        self,
        message: str,
    ):

        self.warnings.append(message)

        self.score -= 5