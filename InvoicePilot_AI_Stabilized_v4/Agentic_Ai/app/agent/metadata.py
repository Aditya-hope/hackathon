"""
Agent execution metadata.

Stores execution statistics, provider information,
and workflow metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class AgentMetadata:
    """
    Metadata collected during the execution
    of the Invoice Agent.
    """

    # ==========================================================
    # EXECUTION INFORMATION
    # ==========================================================

    execution_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    workflow_version: str = "1.0.0"

    request_source: str = "web"

    user_id: str | None = None

    # ==========================================================
    # TIMESTAMPS
    # ==========================================================

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    completed_at: datetime | None = None

    processing_time: float | None = None

    # ==========================================================
    # LLM INFORMATION
    # ==========================================================

    provider_used: str | None = None

    model_used: str | None = None

    confidence: float | None = None

    # ==========================================================
    # EXECUTION METRICS
    # ==========================================================

    provider_attempts: list[str] = field(
        default_factory=list
    )

    retry_count: int = 0

    skill_timings: dict[str, float] = field(
        default_factory=dict
    )

    # ==========================================================
    # METHODS
    # ==========================================================

    def mark_completed(self) -> None:
        """
        Mark workflow completion and calculate
        total execution time.
        """

        self.completed_at = datetime.utcnow()

        self.processing_time = (
            self.completed_at - self.started_at
        ).total_seconds()

    def add_provider_attempt(
        self,
        provider: str,
    ) -> None:
        """
        Record a provider that was attempted.
        """

        self.provider_attempts.append(provider)

    def increment_retry(self) -> None:
        """
        Increment retry counter.
        """

        self.retry_count += 1

    def add_skill_timing(
        self,
        skill: str,
        seconds: float,
    ) -> None:
        """
        Record execution time of a skill.
        """

        self.skill_timings[skill] = seconds

    def set_provider(
        self,
        provider: str,
        model: str,
    ) -> None:
        """
        Record the provider and model that
        successfully processed the request.
        """

        self.provider_used = provider
        self.model_used = model

    def set_confidence(
        self,
        confidence: float,
    ) -> None:
        """
        Store extraction confidence.
        """

        self.confidence = confidence