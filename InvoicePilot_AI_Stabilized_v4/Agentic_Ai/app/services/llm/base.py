from abc import ABC, abstractmethod

from app.documents import Document
from app.schemas.invoice import Invoice


class BaseLLMProvider(ABC):
    """
    Base interface for all supported LLM providers.
    """

    name: str = "base"

    version: str = "1.0.0"

    model: str = ""

    supports_vision: bool = False

    max_tokens: int = 0

    # ---------------------------------------------------------

    @abstractmethod
    def extract_invoice(
        self,
        document: Document,
    ) -> Invoice:
        """
        Extract invoice information.
        """
        raise NotImplementedError

    # ---------------------------------------------------------

    @abstractmethod
    def chat(
        self,
        prompt: str,
    ) -> str:
        """
        Execute a general reasoning request.
        """
        raise NotImplementedError