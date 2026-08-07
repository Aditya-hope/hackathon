"""
Recommendation Package.

Only lightweight, dependency-free members are exported here.
``InvoiceRecommendationEngine`` is intentionally NOT re-exported:
it depends on ``AgentContext``, and importing it at package-init
time would recreate the app.agent <-> app.recommendations circular
import. Import it directly where needed:

    from app.recommendations.invoice_recommendation import (
        InvoiceRecommendationEngine,
    )
"""

from .base import BaseRecommendationEngine

from .recommendation_result import (
    RecommendationDecision,
    RecommendationResult,
)

__all__ = [

    "BaseRecommendationEngine",

    "RecommendationDecision",

    "RecommendationResult",

]