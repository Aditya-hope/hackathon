"""
Duplicate Invoice Detection Package.
"""

from .base import BaseDuplicateDetector

from .duplicate_result import (
    DuplicateMatchType,
    DuplicateResult,
)

from .duplicate_detector import DuplicateInvoiceDetector

__all__ = [

    "BaseDuplicateDetector",

    "DuplicateMatchType",

    "DuplicateResult",

    "DuplicateInvoiceDetector",

]
