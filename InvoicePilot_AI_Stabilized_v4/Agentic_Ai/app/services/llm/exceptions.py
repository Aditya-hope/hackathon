"""
Custom exceptions for the LLM module.
"""


class LLMError(Exception):
    """
    Base exception for all LLM related errors.
    """
    pass


class EmptyDocumentError(LLMError):
    """
    Raised when a document contains no usable content.
    """
    pass


class ProviderUnavailableError(LLMError):
    """
    Raised when an LLM provider is unavailable.
    """
    pass


class RateLimitError(LLMError):
    """
    Raised when the provider rate limit has been exceeded.
    """
    pass


class InvalidResponseError(LLMError):
    """
    Raised when the LLM returns an invalid response.
    """
    pass


class AuthenticationError(LLMError):
    """
    Raised when authentication with the provider fails.
    """
    pass


class RequestTimeoutError(LLMError):
    """
    Raised when the request exceeds the allowed timeout.
    """
    pass


class ProviderConfigurationError(LLMError):
    """
    Raised when a provider is incorrectly configured.
    """
    pass


def classify_provider_error(error: Exception) -> LLMError:
    """
    Map a raw SDK exception (Gemini/Groq/OpenAI-compatible client)
    to one of this module's LLMError subclasses so the router can
    apply the right retry/failover strategy.

    Uses duck-typing instead of importing each SDK's exception
    classes directly, since not every provider SDK may be
    installed in every environment.
    """

    status_code = getattr(error, "status_code", None)

    error_name = type(error).__name__.lower()

    if status_code == 429 or "ratelimit" in error_name:
        return RateLimitError(str(error))

    if status_code == 401 or status_code == 403 or "authentication" in error_name:
        return AuthenticationError(str(error))

    if "timeout" in error_name:
        return RequestTimeoutError(str(error))

    return ProviderUnavailableError(str(error))