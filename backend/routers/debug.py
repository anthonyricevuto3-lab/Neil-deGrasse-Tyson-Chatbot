"""Debug endpoints for verifying LLM/provider configuration at runtime."""

from fastapi import APIRouter
from backend.settings import get_settings

router = APIRouter()

@router.get("/debug/llm")
async def debug_llm():
    settings = get_settings()
    return {
        "provider": settings.model_provider,
        "model": settings.llm_model,
        "openai_key_present": bool(settings.openai_api_key),
        "anthropic_key_present": bool(settings.anthropic_api_key),
    }


@router.get("/debug/cors")
async def debug_cors():
    """Return current CORS origins from server config."""
    settings = get_settings()
    return {
        "cors_origins": settings.cors_origins,
    }
