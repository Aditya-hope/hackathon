"""
Chat API schemas.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    AI Copilot request.
    """

    execution_id: str = Field(
        ...,
        description="Execution ID returned after invoice processing.",
    )

    question: str = Field(
        ...,
        min_length=1,
        description="Natural language question.",
    )


class ChatResponse(BaseModel):
    """
    AI Copilot response.
    """

    answer: str

    provider: str

    confidence: float

    execution_id: str


class ChatMessage(BaseModel):
    """
    A single stored turn in an AI Copilot conversation.
    """

    role: str = Field(
        ...,
        description="'user' or 'assistant'.",
    )

    content: str

    timestamp: str


class ChatHistoryResponse(BaseModel):
    """
    Full stored conversation for a single invoice execution.
    """

    execution_id: str

    messages: list[ChatMessage] = Field(default_factory=list)