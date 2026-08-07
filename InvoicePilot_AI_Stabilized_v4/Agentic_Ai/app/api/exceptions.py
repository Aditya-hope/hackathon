"""
API exception handling.

Maps internal exception hierarchies (document processing, LLM
providers) to clean, consistent HTTP responses instead of letting
raw tracebacks leak to clients.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core import logger

from app.documents.exceptions import (
    DocumentError,
    UnsupportedDocumentError,
    EmptyDocumentError,
)

from app.services.llm.exceptions import (
    LLMError,
    ProviderConfigurationError,
    ProviderUnavailableError,
    RateLimitError,
    AuthenticationError,
)


def _error_response(status_code: int, error_type: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_type,
            "detail": detail,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Attach exception handlers to the FastAPI app.

    Call this once, from app.api.main, right after creating the
    FastAPI instance.
    """

    # ----------------------------------------------------------
    # Document errors -> 400 Bad Request
    # ----------------------------------------------------------

    @app.exception_handler(UnsupportedDocumentError)
    async def unsupported_document_handler(request: Request, exc: UnsupportedDocumentError):
        logger.warning(f"Unsupported document: {exc}")
        return _error_response(400, "unsupported_document", str(exc))

    @app.exception_handler(EmptyDocumentError)
    async def empty_document_handler(request: Request, exc: EmptyDocumentError):
        logger.warning(f"Empty document: {exc}")
        return _error_response(400, "empty_document", str(exc))

    @app.exception_handler(DocumentError)
    async def document_error_handler(request: Request, exc: DocumentError):
        logger.warning(f"Document error: {exc}")
        return _error_response(400, "document_error", str(exc))

    # ----------------------------------------------------------
    # LLM / provider errors -> 502/503/401
    # ----------------------------------------------------------

    @app.exception_handler(ProviderConfigurationError)
    async def provider_configuration_handler(request: Request, exc: ProviderConfigurationError):
        logger.error(f"Provider misconfigured: {exc}")
        return _error_response(503, "provider_not_configured", str(exc))

    @app.exception_handler(AuthenticationError)
    async def provider_auth_handler(request: Request, exc: AuthenticationError):
        logger.error(f"Provider authentication failed: {exc}")
        return _error_response(401, "provider_authentication_failed", str(exc))

    @app.exception_handler(RateLimitError)
    async def provider_rate_limit_handler(request: Request, exc: RateLimitError):
        logger.warning(f"Provider rate limited: {exc}")
        return _error_response(429, "provider_rate_limited", str(exc))

    @app.exception_handler(ProviderUnavailableError)
    async def provider_unavailable_handler(request: Request, exc: ProviderUnavailableError):
        logger.error(f"All providers unavailable: {exc}")
        return _error_response(502, "provider_unavailable", str(exc))

    @app.exception_handler(LLMError)
    async def llm_error_handler(request: Request, exc: LLMError):
        logger.error(f"LLM error: {exc}")
        return _error_response(502, "llm_error", str(exc))

    # ----------------------------------------------------------
    # Fallback -> 500 Internal Server Error
    # ----------------------------------------------------------

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception.")
        return _error_response(500, "internal_error", "An unexpected error occurred.")
