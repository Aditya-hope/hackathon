"""
FastAPI entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import logger, settings
from app.bootstrap import get_application
from app.api.routes import router
from app.api.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.
    """

    logger.info("Starting InvoicePilot AI...")

    # Build dependency graph at startup
    get_application()

    yield

    logger.info("Shutting down InvoicePilot AI.")


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Agentic AI Invoice Processing API",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,

    # Open CORS: this API has no cookie-based auth (the frontend
    # never sends credentials), and the frontend's Settings modal
    # lets a user point at any backend URL from any origin — a
    # fixed allowlist just breaks that. Safe to allow all origins
    # since allow_credentials is off.
    allow_origins=["*"],

    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Exception Handlers
# ==========================================================

register_exception_handlers(app)

# ==========================================================
# API Routes
# ==========================================================

app.include_router(router)

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/", tags=["System"])
def root():

    return {
        "application": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
