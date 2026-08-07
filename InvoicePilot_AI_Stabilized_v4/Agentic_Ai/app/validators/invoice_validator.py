"""
Enterprise Invoice Validator.
"""

from datetime import datetime

from app.schemas.invoice import Invoice

from app.validators.base import BaseValidator

from app.validators.validation_result import (
    ValidationResult,
)


class InvoiceValidator(BaseValidator):

    """
    Validates extracted invoice data.
    """

    def validate(
        self,
        invoice: Invoice,
    ) -> ValidationResult:

        result = ValidationResult()

        # -----------------------------
        # Vendor
        # -----------------------------

        if not invoice.vendor_name:

            result.add_error(
                "Vendor name is missing."
            )

        # -----------------------------
        # Invoice Number
        # -----------------------------

        if not invoice.invoice_number:

            result.add_error(
                "Invoice number is missing."
            )

        # -----------------------------
        # Invoice Date
        # -----------------------------

        if invoice.invoice_date is None:

            result.add_error(
                "Invoice date is missing."
            )

        # -----------------------------
        # Total Amount
        # -----------------------------

        if invoice.total_amount is None:

            result.add_error(
                "Total amount missing."
            )

        elif invoice.total_amount <= 0:

            result.add_error(
                "Invalid total amount."
            )

        # -----------------------------
        # Currency
        # -----------------------------

        if not invoice.currency:

            result.add_warning(
                "Currency not detected."
            )

        # -----------------------------
        # Purchase Order
        # -----------------------------

        if not invoice.purchase_order:

            result.add_warning(
                "Purchase order not found."
            )

        return result