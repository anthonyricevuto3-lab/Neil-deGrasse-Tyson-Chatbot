"""Application settings using Pydantic."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    openai_api_key: str
    anthropic_api_key: str | None = None

    # Model Configuration
    llm_model: str = "gpt-4"
    embedding_model: str = "text-embedding-3-small"
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
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

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
    return Settings()
