"""
Groq Provider.
"""

import json

from app.core import logger, settings
from app.documents import Document
from app.prompts import PromptManager
from app.schemas.invoice import Invoice
from app.services.llm.base import BaseLLMProvider

from app.services.llm import (
    EmptyDocumentError,
    InvalidResponseError,
    ProviderConfigurationError,
    classify_provider_error,
)


class GroqProvider(BaseLLMProvider):
    """
    Groq implementation.
    """

    name = "groq"

    model = settings.GROQ_MODEL

    version = "1.0.0"

    supports_vision = False

    max_tokens = 8192

    def __init__(self):

        if not settings.GROQ_API_KEY:
            raise ProviderConfigurationError(
                "GROQ_API_KEY is not configured."
            )

        try:
            from groq import Groq

        except ImportError as e:
            raise ProviderConfigurationError(
                "The 'groq' package is not installed. "
                "Run: pip install groq"
            ) from e

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    # ---------------------------------------------------------

    def _normalize_invoice_json(
        self,
        content: str,
    ) -> str:
        """
        Normalize common LLM JSON keys to match the Invoice schema.
        """

        data = json.loads(content)

        key_map = {
            "Vendor Name": "vendor_name",
            "Invoice Number": "invoice_number",
            "Invoice Date": "invoice_date",
            "Due Date": "due_date",
            "Currency": "currency",
            "Subtotal": "subtotal",
            "Tax": "tax",
            "Total Amount": "total_amount",
            "GST Number": "gst_number",
            "Purchase Order": "purchase_order",
            "Purchase Order Number": "purchase_order",
            "Payment Terms": "payment_terms",
            "Line Items": "line_items",
            "Confidence": "confidence",
        }

        normalized = {}

        for key, value in data.items():
            normalized[key_map.get(key, key)] = value

        # Normalize line item keys too
        if "line_items" in normalized:

            fixed_items = []

            for item in normalized["line_items"]:

                fixed_items.append(
                    {
                        "description": item.get("description")
                        or item.get("Description"),

                        "quantity": item.get("quantity")
                        or item.get("Quantity", 0),

                        "unit_price": item.get("unit_price")
                        or item.get("Unit Price", 0),

                        "amount": item.get("amount")
                        or item.get("Amount", 0),
                    }
                )

            normalized["line_items"] = fixed_items

        return json.dumps(normalized)

    # ---------------------------------------------------------

    def extract_invoice(
        self,
        document: Document,
    ) -> Invoice:
        """
        Extract invoice information using Groq.
        """

        logger.info(
            f"[{self.name}] Invoice extraction started."
        )

        if not document.text:

            raise EmptyDocumentError(
                "Groq only supports text documents."
            )

        prompt = PromptManager.invoice_extraction()

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                temperature=0,

                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": document.text,
                    },
                ],

                response_format={
                    "type": "json_object"
                }

            )

            content = response.choices[0].message.content

            if not content:

                raise InvalidResponseError(
                    "Groq returned an empty response."
                )

            logger.info("========== RAW GROQ RESPONSE ==========")
            logger.info(content)
            logger.info("=======================================")

            normalized = self._normalize_invoice_json(
                content
            )

            logger.info("======= NORMALIZED RESPONSE ==========")
            logger.info(normalized)
            logger.info("======================================")

            invoice = Invoice.model_validate_json(
                normalized
            )

            logger.info(
                f"[{self.name}] Invoice extraction completed."
            )

            return invoice

        except EmptyDocumentError:
            raise

        except InvalidResponseError:
            raise

        except Exception as e:

            logger.exception(
                f"[{self.name}] Provider failed."
            )

            raise classify_provider_error(e) from e
    # ---------------------------------------------------------

    def chat(
        self,
        prompt: str,
    ) -> str:
        """
        Execute a general AI reasoning request.
        """

        logger.info(
            f"[{self.name}] Chat request started."
        )

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                temperature=0.2,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

            )

            content = response.choices[0].message.content

            if not content:

                raise InvalidResponseError(
                    "Groq returned an empty response."
                )

            logger.info(
                f"[{self.name}] Chat completed."
            )

            return content.strip()

        except InvalidResponseError:
            raise

        except Exception as e:

            logger.exception(
                f"[{self.name}] Chat failed."
            )

            raise classify_provider_error(e) from e