from pydantic import BaseModel, Field
from typing import List, Optional


class AgentResponse(BaseModel):
    """
    Final response produced by InvoicePilot AI.
    """

    status: str = Field(
        ...,
        description="Current processing status"
    )

    recommendation: str = Field(
        ...,
        description="Final recommendation from the agent"
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall confidence score"
    )

    risk: str = Field(
        ...,
        description="Risk assessment"
    )

    reasoning: List[str] = Field(
        default_factory=list,
        description="Explanation of every decision"
    )

    violated_rules: List[str] = Field(
        default_factory=list,
        description="Business rules violated"
    )

    next_action: str = Field(
        ...,
        description="Next workflow step"
    )

    requires_human_review: bool = Field(
        default=False
    )

    metadata: Optional[dict] = Field(
        default_factory=dict
    )