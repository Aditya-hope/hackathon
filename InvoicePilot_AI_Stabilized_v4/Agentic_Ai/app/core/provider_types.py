from enum import Enum


class ProviderType(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"
    NVIDIA = "nvidia"