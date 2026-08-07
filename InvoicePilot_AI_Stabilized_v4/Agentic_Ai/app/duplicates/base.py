"""
Base Duplicate Invoice Detector.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.duplicates.duplicate_result import DuplicateResult

if TYPE_CHECKING:
    from app.schemas.invoice import Invoice


class BaseDuplicateDetector(ABC):
    """
    Storage + matching contract for Duplicate Invoice Detection.
    """

    @abstractmethod
    def check(
        self,
        invoice: "Invoice",
        execution_id: str,
    ) -> DuplicateResult:

        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        invoice: "Invoice",
        execution_id: str,
    ) -> None:

        raise NotImplementedError
