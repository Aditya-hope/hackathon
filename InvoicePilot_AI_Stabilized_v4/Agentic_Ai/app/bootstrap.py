"""
Application Bootstrap.

Creates and wires together all application dependencies
(dependency injection container).
"""

from app.core import logger, settings

from app.agent.invoice_agent import InvoiceAgent

from app.agent.planner import Planner

from app.skills.registry import SkillRegistry

# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

from app.services.llm.llm_service import LLMService
from app.assistant.reasoning_copilot import ReasoningCopilot

# ---------------------------------------------------------
# Business Engines
# ---------------------------------------------------------

from app.validators import InvoiceValidator

from app.policies import InvoicePolicyEngine

from app.risk.invoice_risk import InvoiceRiskEngine

from app.recommendations.invoice_recommendation import (
    InvoiceRecommendationEngine,
)

from app.audit import (
    AuditService,
    AuditLogger,
)

from app.vendors import VendorRepository

from app.duplicates import DuplicateInvoiceDetector

from app.approval import ApprovalQueueService

# ---------------------------------------------------------
# Skills
# ---------------------------------------------------------

from app.skills import (
    ExtractInvoiceSkill,
    VendorLookupSkill,
    ValidateInvoiceSkill,
    DuplicateDetectionSkill,
    PolicyEngineSkill,
    RiskAssessmentSkill,
    RecommendationSkill,
    ApprovalQueueSkill,
    AuditLoggerSkill,
)


class Application:
    """
    Dependency Injection Container.
    """

    def __init__(self):

        logger.info(
            f"Bootstrapping {settings.APP_NAME} "
            f"v{settings.APP_VERSION} ({settings.ENVIRONMENT})"
        )

        # =====================================================
        # Services
        # =====================================================

        self.llm_service = LLMService()
        # =====================================================
        # AI Assistant
        # =====================================================

        self.reasoning_copilot = ReasoningCopilot(
            self.llm_service
            )

        configured = settings.configured_providers()

        if configured:
            logger.info(
                f"LLM providers configured: {', '.join(configured)}"
            )

        # =====================================================
        # Business Engines
        # =====================================================

        self.validator = InvoiceValidator()

        self.policy_engine = InvoicePolicyEngine()

        self.risk_engine = InvoiceRiskEngine()

        self.recommendation_engine = (
            InvoiceRecommendationEngine()
        )

        self.audit_service = AuditService()

        self.audit_logger = AuditLogger()

        self.vendor_repository = VendorRepository()

        self.duplicate_detector = DuplicateInvoiceDetector()

        self.approval_queue = ApprovalQueueService()

        # =====================================================
        # Registry
        # =====================================================

        self.registry = SkillRegistry()

        # =====================================================
        # Register Skills
        # =====================================================

        self.registry.register(

            ExtractInvoiceSkill(
                self.llm_service
            )

        )

        self.registry.register(

            VendorLookupSkill(
                self.vendor_repository
            )

        )

        self.registry.register(

            ValidateInvoiceSkill(
                self.validator
            )

        )

        self.registry.register(

            DuplicateDetectionSkill(
                self.duplicate_detector
            )

        )

        self.registry.register(

            PolicyEngineSkill(
                self.policy_engine
            )

        )

        self.registry.register(

            RiskAssessmentSkill(
                self.risk_engine
            )

        )

        self.registry.register(

            RecommendationSkill(
                self.recommendation_engine
            )

        )

        self.registry.register(

            ApprovalQueueSkill(
                self.approval_queue
            )

        )

        self.registry.register(

            AuditLoggerSkill(

                self.audit_service,

                self.audit_logger,

            )

        )

        # =====================================================
        # Planner
        # =====================================================

        self.planner = Planner()

        # =====================================================
        # Agent
        # =====================================================

        self.agent = InvoiceAgent(

            planner=self.planner,

            registry=self.registry,

        )

        logger.info(
            f"Application ready. Registered skills: "
            f"{', '.join(self.registry.list_skills())}"
        )


# ---------------------------------------------------------
# Factory Function
# ---------------------------------------------------------

_app = None


def get_application() -> Application:
    """
    Returns a singleton Application instance.
    """

    global _app

    if _app is None:

        _app = Application()

    return _app


def get_agent() -> InvoiceAgent:

    """
    Returns the configured Invoice Agent.
    """

    return get_application().agent

def get_reasoning_copilot() -> ReasoningCopilot:
    """
    Returns the configured AI Copilot.
    """

    return get_application().reasoning_copilot

def reset_application() -> None:
    """
    Clear the cached Application singleton.

    Mainly useful for tests that need a fresh dependency graph
    (e.g. after changing environment variables).
    """

    global _app

    _app = None