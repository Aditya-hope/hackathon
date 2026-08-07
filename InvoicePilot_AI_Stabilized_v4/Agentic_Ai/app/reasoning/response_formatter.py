"""
Response Formatter.

Formats AI responses into a consistent API response.
"""

from app.schemas.chat import ChatResponse


class ResponseFormatter:
    """
    Formats AI responses returned by the LLM.
    """

    def format(
        self,
        answer: str,
        execution_id: str,
        provider: str = "unknown",
        confidence: float = 1.0,
    ) -> ChatResponse:

        return ChatResponse(

            answer=answer.strip(),

            provider=provider,

            confidence=confidence,

            execution_id=execution_id,

        )