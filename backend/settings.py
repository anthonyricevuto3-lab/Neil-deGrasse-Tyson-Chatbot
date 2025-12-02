"""Application settings using Pydantic."""

from functools import lru_cache
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    openai_api_key: str
    anthropic_api_key: str | None = None  # Optional, only needed if using Anthropic provider

    # Model Configuration
    llm_model: str = "gpt-4o-mini"
    model_provider: str = "openai"  # "anthropic" or "openai"
    embedding_model: str = "text-embedding-3-large"
    temperature: float = 0.7

    # RAG Configuration
    top_k: int = 10
    rerank_top_k: int = 5
    chunk_size: int = 512
    chunk_overlap: int = 50

    # Vector Store
    vector_store_path: str = "storage/vector_store"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:5173,https://polite-sand-06dd6b31e.3.azurestaticapps.net,https://neil-degrasse-tyson-ai-chatbot.com,https://www.neil-degrasse-tyson-ai-chatbot.com"

    # Logging
    log_level: str = "INFO"

    # Guardrails
    max_response_words: int = 300
    require_citations: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    return settings


def get_cors_origins() -> list[str]:
    """Parse CORS origins from settings."""
    settings = get_settings()
    if isinstance(settings.cors_origins, str):
        return [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    return settings.cors_origins
