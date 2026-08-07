"""
Enterprise LLM Service.

Acts as the single entry point for
all LLM operations.
"""

from app.core import logger
from app.documents import Document
from app.schemas.invoice import Invoice

from app.services.llm.router import LLMRouter

from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.groq_provider import GroqProvider
from app.services.llm.nvidia_provider import NvidiaProvider

from app.services.llm.exceptions import ProviderConfigurationError


PROVIDER_CLASSES = {
    "gemini": GeminiProvider,
    "groq": GroqProvider,
    "nvidia": NvidiaProvider,
}


class LLMService:
    """
    Enterprise LLM Service.

    Encapsulates provider initialization
    and intelligent routing.
    """

    def __init__(self):

        providers = {}

        for name, provider_cls in PROVIDER_CLASSES.items():

            try:
                providers[name] = provider_cls()

            except ProviderConfigurationError as e:
                # A missing API key shouldn't stop the whole
                # application from starting - just disable that
                # one provider. The router will simply skip it.
                logger.warning(
                    f"Provider '{name}' disabled: {e}"
                )

        if not providers:
            logger.warning(
                "No LLM providers are configured. "
                "Invoice extraction will fail until at least one "
                "API key is set."
            )

        self.router = LLMRouter(
            providers=providers
        )

    # -----------------------------------------------------

    def extract_invoice(
        self,
        document: Document,
    ) -> tuple[Invoice, str, str]:
        """
        Extract structured invoice data.

        Returns:
            (invoice, provider_name, model_name)
        """

        return self.router.extract_invoice(
            document
        )
    # -----------------------------------------------------

    def chat(
        self,
        prompt: str,
    ) -> tuple[str, str, str]:
        """
        Execute a reasoning request.

        Returns:
            (answer, provider_name, model_name)
        """

        return self.router.chat(
            prompt
        )