"""
Enterprise Invoice Policy Engine.
"""

from app.schemas.invoice import Invoice

from app.policies.base import BasePolicyEngine

from app.policies.policy_result import PolicyResult


class InvoicePolicyEngine(BasePolicyEngine):

    def evaluate(
        self,
        invoice: Invoice,
    ) -> PolicyResult:

        result = PolicyResult()

        # ----------------------------------------
        # Rule 1
        # ----------------------------------------

        if (
            invoice.total_amount
            and invoice.total_amount > 50000
            and not invoice.purchase_order
        ):

            result.add_violation(
                "Purchase Order required for invoices above ₹50,000."
            )

        # ----------------------------------------
        # Rule 2
        # ----------------------------------------

        if not invoice.gst_number:

            result.mark_for_review()

            result.add_recommendation(
                "GST number missing."
            )

        # ----------------------------------------
        # Rule 3
        # ----------------------------------------

        if invoice.currency != "INR":

            result.mark_for_review()

            result.add_recommendation(
                "Foreign currency invoice."
            )

        return result