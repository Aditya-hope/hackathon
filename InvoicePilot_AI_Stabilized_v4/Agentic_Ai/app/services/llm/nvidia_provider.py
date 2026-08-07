"""
NVIDIA NIM Provider.
"""

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


class NvidiaProvider(BaseLLMProvider):
    """
    NVIDIA NIM implementation.
    """

    name = "nvidia"

    model = settings.NVIDIA_MODEL

    version = "1.0.0"

    supports_vision = False

    max_tokens = 8192

    def __init__(self):

        if not settings.NVIDIA_API_KEY:
            raise ProviderConfigurationError(
                "NVIDIA_API_KEY is not configured."
            )

        try:
            from openai import OpenAI

        except ImportError as e:
            raise ProviderConfigurationError(
                "The 'openai' package is not installed. "
                "Run: pip install openai"
            ) from e

        self.client = OpenAI(

            api_key=settings.NVIDIA_API_KEY,

            base_url="https://integrate.api.nvidia.com/v1"

        )

    def extract_invoice(
        self,
        document: Document,
    ) -> Invoice:
        """
        Extract invoice information using NVIDIA NIM.
        """

        logger.info(
            f"[{self.name}] Invoice extraction started."
        )

        if not document.text:

            raise EmptyDocumentError(
                "NVIDIA provider currently supports text documents only."
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
                ]

            )

            content = response.choices[0].message.content

            if not content:

                raise InvalidResponseError(
                    "NVIDIA returned an empty response."
                )

            invoice = Invoice.model_validate_json(
                content
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
        Execute a general reasoning request.
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
                    "NVIDIA returned an empty response."
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