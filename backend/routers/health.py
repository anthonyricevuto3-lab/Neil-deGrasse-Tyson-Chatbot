"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz():
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness():
    """Readiness check (includes dependencies)."""
    # TODO: Check vector store, LLM connectivity, etc.
    return {
        "status": "ready",
        "vector_store": "ok",
        "llm": "ok",
    }
