"""
Prompt Manager.

Responsible for constructing prompts used
throughout InvoicePilot AI.
"""

from app.prompts.system import SYSTEM_PROMPT

from app.prompts.invoice_extraction import (
    INVOICE_EXTRACTION_PROMPT,
)

from app.prompts.validation import (
    VALIDATION_PROMPT,
)

from app.prompts.policy import (
    POLICY_PROMPT,
)

from app.prompts.recommendation import (
    RECOMMENDATION_PROMPT,
)


class PromptManager:
    """
    Builds prompts for all AI tasks.
    """

    @staticmethod
    def invoice_extraction() -> str:
        """
        Build invoice extraction prompt.
        """

        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"{INVOICE_EXTRACTION_PROMPT}"
        )

    @staticmethod
    def validation() -> str:
        """
        Build validation prompt.
        """

        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"{VALIDATION_PROMPT}"
        )

    @staticmethod
    def policy() -> str:
        """
        Build policy evaluation prompt.
        """

        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"{POLICY_PROMPT}"
        )

    @staticmethod
    def recommendation() -> str:
        """
        Build recommendation prompt.
        """

        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"{RECOMMENDATION_PROMPT}"
        )