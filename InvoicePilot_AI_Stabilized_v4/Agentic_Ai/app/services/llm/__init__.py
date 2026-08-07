"""
LLM Provider Package.
"""

from .base import BaseLLMProvider
from .exceptions import (
    LLMError,
    EmptyDocumentError,
    ProviderUnavailableError,
    RateLimitError,
    InvalidResponseError,
    AuthenticationError,
    RequestTimeoutError,
    ProviderConfigurationError,
    classify_provider_error,
)

__all__ = [

    "BaseLLMProvider",

    "LLMError",

    "EmptyDocumentError",

    "ProviderUnavailableError",

    "RateLimitError",

    "InvalidResponseError",

    "AuthenticationError",

    "RequestTimeoutError",

    "ProviderConfigurationError",

    "classify_provider_error",

]