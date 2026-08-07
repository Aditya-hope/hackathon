"""
Enterprise Intelligent LLM Router.

Responsible for:
- Intelligent provider selection
- Automatic failover
- Retry handling
- Provider abstraction
"""

from typing import Dict, List

from app.core import (
    logger,
    settings,
)

from app.documents import Document
from app.schemas.invoice import Invoice

from app.services.llm.base import BaseLLMProvider

from app.services.llm.exceptions import (
    EmptyDocumentError,
    ProviderUnavailableError,
    RateLimitError,
    RequestTimeoutError,
)


class LLMRouter:
    """
    Enterprise Intelligent Router.

    Routes requests to the best available
    LLM provider.
    """

    def __init__(
        self,
        providers: Dict[str, BaseLLMProvider],
    ):

        self.providers = providers

    # ---------------------------------------------------------

    def _provider_order(
        self,
        document: Document,
    ) -> List[BaseLLMProvider]:
        """
        Determine provider priority based on document type.

        Only providers that are actually registered (i.e. had a
        valid API key at startup) are included; a missing or
        misconfigured provider is skipped rather than raising, so
        failover can still proceed to whatever is available.
        """

        if document.content:

            logger.info(
                "Vision document detected."
            )

            primary = settings.VISION_PROVIDER

        else:

            logger.info(
                "Text document detected."
            )

            primary = settings.TEXT_PROVIDER

        candidate_names = [primary] + [
            name
            for name in settings.FALLBACK_PROVIDERS
            if name != primary
        ]

        ordered = [
            self.providers[name]
            for name in candidate_names
            if name in self.providers
        ]

        if not ordered:
            raise ProviderUnavailableError(
                "No LLM providers are configured/available."
            )

        return ordered

    # ---------------------------------------------------------

    def extract_invoice(
        self,
        document: Document,
    ) -> tuple[Invoice, str, str]:
        """
        Extract invoice using the best available provider.

        Returns:
            (invoice, provider_name, model_name)
        """

        providers = self._provider_order(
            document
        )

        last_exception = None

        for provider in providers:

            logger.info(
                f"Trying provider: {provider.name}"
            )

            retry = 0

            while retry <= settings.MAX_PROVIDER_RETRIES:

                try:

                    invoice = provider.extract_invoice(
                        document
                    )

                    logger.info(
                        f"{provider.name} succeeded."
                    )

                    return (
                                invoice,
                                provider.name,
                                provider.model,
                            )

                except EmptyDocumentError:

                    logger.error(
                        "Document contains no usable content."
                    )

                    raise

                except RateLimitError as e:

                    logger.warning(
                        f"{provider.name} rate limited."
                    )

                    last_exception = e

                    break

                except RequestTimeoutError as e:

                    retry += 1

                    logger.warning(
                        f"{provider.name} timeout "
                        f"({retry}/{settings.MAX_PROVIDER_RETRIES})"
                    )

                    if retry > settings.MAX_PROVIDER_RETRIES:

                        last_exception = e

                        break

                except ProviderUnavailableError as e:

                    logger.warning(
                        f"{provider.name} unavailable."
                    )

                    last_exception = e

                    break

                except Exception as e:

                    import traceback

                    traceback.print_exc()

                    print("\n" + "=" * 80)
                    print("REAL EXCEPTION")
                    print("Type :", type(e).__name__)
                    print("Error:", str(e))
                    print("=" * 80 + "\n")

                    logger.exception(
                        f"{provider.name} failed."
                    )

                    last_exception = e

                    break

        logger.error(
            "All providers failed."
        )

        raise ProviderUnavailableError(
            "All configured LLM providers failed."
        ) from last_exception
    # ---------------------------------------------------------

    def chat(
        self,
        prompt: str,
    ) -> tuple[str, str, str]:
        """
        Execute a general chat request using the
        best available provider.

        Returns:
            (answer, provider_name, model_name)
        """

        if not self.providers:

            raise ProviderUnavailableError(
                "No LLM providers are configured."
            )

        candidate_names = [
            settings.TEXT_PROVIDER
        ] + [
            name
            for name in settings.FALLBACK_PROVIDERS
            if name != settings.TEXT_PROVIDER
        ]

        last_exception = None

        for provider_name in candidate_names:

            if provider_name not in self.providers:
                continue

            provider = self.providers[provider_name]

            logger.info(
                f"Trying chat provider: {provider.name}"
            )

            try:

                answer = provider.chat(prompt)

                logger.info(
                    f"{provider.name} chat succeeded."
                )

                return (
                    answer,
                    provider.name,
                    provider.model,
                )

            except Exception as e:

                logger.exception(
                    f"{provider.name} chat failed."
                )

                last_exception = e

                continue

        raise ProviderUnavailableError(
            "All configured providers failed."
        ) from last_exception