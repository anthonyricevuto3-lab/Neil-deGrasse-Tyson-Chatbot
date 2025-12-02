"""Debug endpoints for verifying LLM/provider configuration at runtime."""

from fastapi import APIRouter
from backend.settings import get_settings, get_cors_origins

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
    return {
        "cors_origins": get_cors_origins(),
        "cors_origins_raw": get_settings().cors_origins,
    }
