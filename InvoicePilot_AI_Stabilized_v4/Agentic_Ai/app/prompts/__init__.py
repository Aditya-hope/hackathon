"""
Prompt templates used throughout InvoicePilot AI.
"""

from .prompt_manager import PromptManager

from .system import SYSTEM_PROMPT

from .invoice_extraction import (
    INVOICE_EXTRACTION_PROMPT,
)

from .validation import (
    VALIDATION_PROMPT,
)

from .policy import (
    POLICY_PROMPT,
)

from .recommendation import (
    RECOMMENDATION_PROMPT,
)

__all__ = [

    "PromptManager",

    "SYSTEM_PROMPT",

    "INVOICE_EXTRACTION_PROMPT",

    "VALIDATION_PROMPT",

    "POLICY_PROMPT",

    "RECOMMENDATION_PROMPT",

]