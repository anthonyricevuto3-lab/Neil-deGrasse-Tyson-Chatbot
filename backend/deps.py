"""Shared dependencies and lazy-loaded singletons."""

from functools import lru_cache

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from backend.settings import get_settings


@lru_cache
def get_llm() -> ChatOpenAI:
    """Get cached LLM client."""
    settings = get_settings()
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.temperature,
        api_key=settings.openai_api_key,
    )


@lru_cache
def get_embeddings() -> OpenAIEmbeddings:
    """Get cached embeddings client."""
    settings = get_settings()
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
