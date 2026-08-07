"""
Agent execution context.

Shared state that flows through every skill
during invoice processing.
"""

from __future__ import annotations

import uuid

from dataclasses import dataclass, field

from app.agent.event import AgentEvent
from app.agent.metadata import AgentMetadata
from app.agent.state import AgentState

from app.documents import Document

from app.schemas.invoice import Invoice

from app.validators.validation_result import ValidationResult
from app.policies.policy_result import PolicyResult
from app.risk.risk_result import RiskResult
from app.recommendations.recommendation_result import (
    RecommendationResult,
)
from app.vendors.vendor_result import VendorLookupResult
from app.duplicates.duplicate_result import DuplicateResult


@dataclass
class AgentContext:
    """
    Shared execution context for the Invoice Agent.
    """

    # ==========================================================
    # INPUT
    # ==========================================================

    document: Document

    # ==========================================================
    # WORKFLOW
    # ==========================================================

    state: AgentState = AgentState.IDLE

    current_skill: str = ""

    completed: bool = False

    # ==========================================================
    # AI COPILOT
    # ==========================================================

    # Unique execution id for every workflow.
    # The AI Copilot uses this id to retrieve
    # the processed invoice later.
   

    # ==========================================================
    # BUSINESS RESULTS
    # ==========================================================

    invoice: Invoice | None = None

    vendor_result: VendorLookupResult | None = None

    validation_result: ValidationResult | None = None

    duplicate_result: DuplicateResult | None = None

    policy_result: PolicyResult | None = None

    risk_result: RiskResult | None = None

    recommendation_result: RecommendationResult | None = None

    # ==========================================================
    # EXECUTION HISTORY
    # ==========================================================

    events: list[AgentEvent] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    metadata: AgentMetadata = field(
        default_factory=AgentMetadata
    )

    # ==========================================================
    # WORKFLOW
    # ==========================================================
    def set_state(
        self,
        state: AgentState,
    ) -> None:

        self.state = state


    def set_current_skill(
        self,
        skill: str,
    ) -> None:

        self.current_skill = skill


    def mark_completed(self) -> None:

        self.completed = True

        self.state = AgentState.COMPLETED

        self.metadata.mark_completed()


    def mark_failed(self) -> None:

        self.completed = False

        self.state = AgentState.FAILED

        self.metadata.mark_completed()


    # ==========================================================
    # BUSINESS RESULTS
    # ==========================================================

    def set_invoice(
        self,
        invoice: Invoice,
    ) -> None:

        self.invoice = invoice


    def set_vendor_result(
        self,
        result: VendorLookupResult,
    ) -> None:

        self.vendor_result = result

        if result.is_blocked:

            self.add_error(
                f"Vendor '{result.vendor.name}' is blocked."
            )

        elif result.is_new_vendor:

            self.add_warning(
                f"New vendor: {result.reason}"
            )


    def set_duplicate_result(
        self,
        result: DuplicateResult,
    ) -> None:

        self.duplicate_result = result

        if result.is_duplicate:

            self.add_warning(
                f"Duplicate invoice suspected: {result.reason}"
            )


    def set_validation_result(
        self,
        result: ValidationResult,
    ) -> None:

        self.validation_result = result

        self.warnings.extend(result.warnings)

        self.errors.extend(result.errors)


    def set_policy_result(
        self,
        result: PolicyResult,
    ) -> None:

        self.policy_result = result

        self.warnings.extend(result.recommendations)

        self.errors.extend(result.violations)


    def set_risk_result(
        self,
        result: RiskResult,
    ) -> None:

        self.risk_result = result


    def set_recommendation_result(
        self,
        result: RecommendationResult,
    ) -> None:

        self.recommendation_result = result


    # ==========================================================
    # EVENTS
    # ==========================================================

    def add_event(
        self,
        skill: str,
        message: str,
        status: str = "SUCCESS",
    ) -> None:

        self.events.append(

            AgentEvent(

                skill=skill,

                state=self.state.value,

                message=message,

                status=status,

            )

        )


    # ==========================================================
    # WARNINGS / ERRORS
    # ==========================================================

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)


    def add_error(
        self,
        message: str,
    ) -> None:

        self.errors.append(message)


    # ==========================================================
    # METADATA
    # ==========================================================

    def set_provider(
        self,
        provider: str,
        model: str,
    ) -> None:

        self.metadata.set_provider(
            provider,
            model,
        )


    def set_confidence(
        self,
        confidence: float,
    ) -> None:

        self.metadata.set_confidence(
            confidence,
        )


    def add_provider_attempt(
        self,
        provider: str,
    ) -> None:

        self.metadata.add_provider_attempt(
            provider,
        )


    def increment_retry_count(
        self,
    ) -> None:

        self.metadata.increment_retry()


    def add_skill_timing(
        self,
        skill: str,
        seconds: float,
    ) -> None:

        self.metadata.add_skill_timing(
            skill,
            seconds,
        )


    # ==========================================================
    # HELPER PROPERTIES
    # ==========================================================
    @property
    def is_valid(self) -> bool:

        return (
            self.validation_result is None
            or self.validation_result.valid
        )


    @property
    def requires_review(self) -> bool:
        """
        Returns True whenever the invoice requires
        manual review.
        """

        if self.policy_result is None:
            return False

        return (
            self.policy_result.requires_review
            or self.policy_result.rejected
        )


    @property
    def is_new_vendor(self) -> bool:

        return bool(
            self.vendor_result
            and self.vendor_result.is_new_vendor
        )


    @property
    def is_blocked_vendor(self) -> bool:

        return bool(
            self.vendor_result
            and self.vendor_result.is_blocked
        )


    @property
    def is_duplicate(self) -> bool:

        return bool(
            self.duplicate_result
            and self.duplicate_result.is_duplicate
        )


    @property
    def risk_score(self) -> float:

        return (
            self.risk_result.score
            if self.risk_result
            else 0.0
        )


    @property
    def risk_level(self):

        return (
            self.risk_result.level
            if self.risk_result
            else None
        )


    @property
    def recommendation(self):

        return (
            self.recommendation_result.decision
            if self.recommendation_result
            else None
        )


    @property
    def has_errors(self) -> bool:

        return bool(self.errors)


    @property
    def has_warnings(self) -> bool:

        return bool(self.warnings)


    @property
    def error_count(self) -> int:

        return len(self.errors)


    @property
    def warning_count(self) -> int:

        return len(self.warnings)


    @property
    def event_count(self) -> int:

        return len(self.events)