"""
Context Builder.

Converts AgentContext into structured data
for the AI Copilot.
"""

from app.agent.context import AgentContext


class ContextBuilder:
    """
    Builds structured LLM context.
    """

    def build(
        self,
        context: AgentContext,
    ) -> dict:

        invoice = context.invoice

        vendor = context.vendor_result

        validation = context.validation_result

        duplicate = context.duplicate_result

        policy = context.policy_result

        risk = context.risk_result

        recommendation = context.recommendation_result

        return {

            # -------------------------------------------------
            # Invoice
            # -------------------------------------------------

            "invoice": {

                "vendor_name": getattr(invoice, "vendor_name", None),

                "invoice_number": getattr(invoice, "invoice_number", None),

                "invoice_date": getattr(invoice, "invoice_date", None),

                "due_date": getattr(invoice, "due_date", None),

                "currency": getattr(invoice, "currency", None),

                "subtotal": getattr(invoice, "subtotal", None),

                "tax": getattr(invoice, "tax", None),

                "total_amount": getattr(invoice, "total_amount", None),

                "purchase_order": getattr(invoice, "purchase_order", None),

                "payment_terms": getattr(invoice, "payment_terms", None),

            },

            # -------------------------------------------------
            # Vendor
            # -------------------------------------------------

            "vendor": {

                "is_new_vendor": getattr(vendor, "is_new_vendor", None),

                "is_blocked": getattr(vendor, "is_blocked", None),

                "reason": getattr(vendor, "reason", None),

            },

            # -------------------------------------------------
            # Validation
            # -------------------------------------------------

            "validation": {

                "valid": getattr(validation, "valid", None),

                "warnings": getattr(validation, "warnings", []),

                "errors": getattr(validation, "errors", []),

            },

            # -------------------------------------------------
            # Duplicate
            # -------------------------------------------------

            "duplicate": {

                "is_duplicate": getattr(duplicate, "is_duplicate", None),

                "reason": getattr(duplicate, "reason", None),

            },

            # -------------------------------------------------
            # Policy
            # -------------------------------------------------

            "policy": {

                "decision": getattr(policy, "decision", None),

                "violations": getattr(policy, "violations", []),

                "recommendations": getattr(policy, "recommendations", []),

            },

            # -------------------------------------------------
            # Risk
            # -------------------------------------------------

            "risk": {

                "score": getattr(risk, "score", None),

                "level": str(getattr(risk, "level", "")),

                "reasons": getattr(risk, "reasons", []),

            },

            # -------------------------------------------------
            # Recommendation
            # -------------------------------------------------

            "recommendation": {

                "decision": str(getattr(recommendation, "decision", "")),

                "reason": getattr(recommendation, "reason", None),

            },

            # -------------------------------------------------
            # Workflow
            # -------------------------------------------------

            "warnings": context.warnings,

            "errors": context.errors,

            "events": [

                {

                    "skill": event.skill,

                    "status": event.status,

                    "message": event.message,

                }

                for event in context.events

            ],

        }