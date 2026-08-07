"""
Application configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings.
    """

    # ==========================================================
    # API KEYS
    # ==========================================================

    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""

    # ==========================================================
    # MODELS
    # ==========================================================

    # Gemini (kept as fallback)
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"

    # Groq (Primary)
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # NVIDIA
    NVIDIA_MODEL: str = "meta/llama-3.3-70b-instruct"

    # ==========================================================
    # PROVIDER ROUTING
    # ==========================================================

    # Groq will be used first
    PRIMARY_PROVIDER: str = "groq"

    # All text extraction goes to Groq
    TEXT_PROVIDER: str = "groq"

    # Vision also uses Groq for now
    # (change back to Gemini later if needed)
    VISION_PROVIDER: str = "groq"

    # Automatic failover order
    FALLBACK_PROVIDERS: list[str] = [
        "gemini",
        "nvidia",
    ]

    # ==========================================================
    # GENERATION SETTINGS
    # ==========================================================

    TEMPERATURE: float = 0.0

    MAX_OUTPUT_TOKENS: int = 8192

    # ==========================================================
    # PROVIDER SETTINGS
    # ==========================================================

    MAX_PROVIDER_RETRIES: int = 2

    # ==========================================================
    # LOGGING
    # ==========================================================

    LOG_LEVEL: str = "INFO"

    # ==========================================================
    # APPLICATION
    # ==========================================================

    APP_NAME: str = "InvoicePilot AI"

    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"

    # ==========================================================
    # PYDANTIC SETTINGS
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================================================
    # HELPERS
    # ==========================================================

    def configured_providers(self) -> list[str]:

        keys = {
            "gemini": self.GEMINI_API_KEY,
            "groq": self.GROQ_API_KEY,
            "nvidia": self.NVIDIA_API_KEY,
        }

        return [
            name
            for name, key in keys.items()
            if key
        ]


settings = Settings()