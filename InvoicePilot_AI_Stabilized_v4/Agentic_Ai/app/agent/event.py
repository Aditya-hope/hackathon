"""
Agent Event Model.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentEvent:
    """
    Represents one execution event.
    """

    skill: str

    state: str

    message: str

    status: str = "SUCCESS"

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )