"""
Google Gemini Provider.
"""

from app.core import logger, settings

from app.documents import Document

from app.prompts.prompt_manager import PromptManager

from app.schemas.invoice import Invoice

from app.services.llm.base import BaseLLMProvider
from app.services.llm import (
    EmptyDocumentError,
    InvalidResponseError,
    ProviderConfigurationError,
    classify_provider_error,
)


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini implementation.
    """

    name = "gemini"

    model = settings.GEMINI_MODEL

    version = "1.0.0"

    supports_vision = True

    max_tokens = 65536

    def __init__(self):

        if not settings.GEMINI_API_KEY:
            raise ProviderConfigurationError(
                "GEMINI_API_KEY is not configured."
            )

        try:
            from google import genai
            from google.genai import types

        except ImportError as e:
            raise ProviderConfigurationError(
                "The 'google-genai' package is not installed. "
                "Run: pip install google-genai"
            ) from e

        self._genai = genai
        self._types = types

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def extract_invoice(
        self,
        document: Document,
    ) -> Invoice:
        """
        Extract structured invoice information
        using Google Gemini.
        """

        logger.info(
            f"[{self.name}] Invoice extraction started."
        )

        prompt = PromptManager.invoice_extraction()

        try:

            # -------------------------------
            # Plain Text Document
            # -------------------------------

            if document.text:

                contents = [
                    prompt,
                    document.text,
                ]

            # -------------------------------
            # Image Document
            # -------------------------------

            elif document.content:

                contents = [
                    prompt,
                    self._types.Part.from_bytes(
                        data=document.content,
                        mime_type=document.mime_type,
                    ),
                ]

            # -------------------------------
            # Empty Document
            # -------------------------------

            else:

                raise EmptyDocumentError(
                    "Document contains no usable content."
                )

            response = self.client.models.generate_content(

                model=self.model,

                contents=contents,

                config=self._types.GenerateContentConfig(

                    temperature=0,

                    response_mime_type="application/json",

                    response_schema=Invoice,

                ),

            )

            if response.parsed is None:

                raise InvalidResponseError(
                    "Gemini returned an empty response."
                )

            logger.info(
                f"[{self.name}] Invoice extraction completed."
            )

            return response.parsed

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
        Execute a general reasoning request.
        """

        logger.info(
            f"[{self.name}] Chat request started."
        )

        try:

            response = self.client.models.generate_content(

                model=self.model,

                contents=prompt,

                config=self._types.GenerateContentConfig(

                    temperature=0.2,

                ),

            )

            if not response.text:

                raise InvalidResponseError(
                    "Gemini returned an empty response."
                )

            logger.info(
                f"[{self.name}] Chat completed."
            )

            return response.text.strip()

        except InvalidResponseError:
            raise

        except Exception as e:

            logger.exception(
                f"[{self.name}] Chat failed."
            )

            raise classify_provider_error(e) from e