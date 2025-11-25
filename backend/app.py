"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import chat, health, search, sources
from backend.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="NDT Bot API",
    description="RAG-powered chatbot in the style of Neil deGrasse Tyson",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(sources.router, prefix="/api", tags=["sources"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NDT Bot API",
        "version": "0.1.0",
        "docs": "/docs",
    }
