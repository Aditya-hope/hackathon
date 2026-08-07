"""
Prompt Builder.

Builds the final prompt that is sent to the LLM.
"""

import json
from typing import Optional

from app.prompts.chat_prompt import SYSTEM_PROMPT


class PromptBuilder:
    """
    Combines:

    - System Prompt
    - Prior conversation history (for this invoice execution)
    - Invoice Context
    - User Question
    """

    def build(
        self,
        context: dict,
        question: str,
        history: Optional[list[dict]] = None,
    ) -> str:
        """
        Build the final prompt.

        ``history`` is the recent turns of this conversation
        (oldest first), each shaped like
        ``{"role": "user" | "assistant", "content": str}``. It lets
        the model resolve follow-up questions ("what about its
        tax?", "why not the second one?") against what was already
        discussed, instead of treating every question in isolation.
        """

        return f"""
{SYSTEM_PROMPT}

==================================================
CONVERSATION HISTORY
==================================================

{self._format_history(history)}

==================================================
INVOICE CONTEXT
==================================================

{json.dumps(context, default=str, indent=2)}

==================================================
USER QUESTION
==================================================

{question}

==================================================
INSTRUCTIONS
==================================================

Answer ONLY using the invoice context above.

Use the conversation history to understand follow-up questions,
pronouns, and references to things already discussed ("that
amount", "the same vendor", "what about the risk score"), and to
stay consistent with what you already told the user - but never
treat something said earlier in the conversation as new invoice
data. The invoice context above is always the source of truth for
facts about the invoice.

If the answer cannot be determined from the supplied context,
clearly say so.

Do not invent information.

Explain your reasoning clearly.
"""

    # ----------------------------------------------------------

    def _format_history(
        self,
        history: Optional[list[dict]],
    ) -> str:

        if not history:

            return "(No previous messages in this conversation yet.)"

        lines = []

        for turn in history:

            role = turn.get("role")

            speaker = "User" if role == "user" else "Assistant"

            content = (turn.get("content") or "").strip()

            if content:

                lines.append(f"{speaker}: {content}")

        return "\n".join(lines) if lines else (
            "(No previous messages in this conversation yet.)"
        )
