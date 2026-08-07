"""
Enterprise AI Guardrails.

Protects the AI Copilot against prompt injection,
secret extraction, and jailbreak attempts.
"""


class Guardrails:
    """
    Security guardrails.

    Only blocks malicious requests.
    It does NOT restrict normal user questions.
    """

    BLOCKED_PHRASES = [

        # Prompt Injection
        "ignore previous instructions",
        "ignore all previous instructions",
        "forget previous instructions",
        "developer prompt",
        "system prompt",
        "reveal prompt",
        "show prompt",

        # Secrets
        "api key",
        "token",
        "password",
        "secret",
        "environment variable",

        # Jailbreak
        "jailbreak",
        "bypass safety",
        "disable guardrails",
        "disable safety",

    ]

    def validate(
        self,
        question: str,
    ) -> tuple[bool, str]:
        """
        Validate a user question.

        Returns:
            (allowed, message)
        """

        q = question.lower()

        # -----------------------------------------
        # Block malicious requests
        # -----------------------------------------

        for phrase in self.BLOCKED_PHRASES:

            if phrase in q:

                return (
                    False,
                    "For security reasons I can't help with that request.",
                )

        # -----------------------------------------
        # Everything else is allowed
        # -----------------------------------------

        return (
            True,
            "",
        )