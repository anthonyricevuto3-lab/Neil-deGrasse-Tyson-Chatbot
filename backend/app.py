"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import chat, health, search, sources, debug
from backend.settings import get_settings, get_cors_origins

settings = get_settings()
cors_origins = get_cors_origins()

app = FastAPI(
    title="NDT Bot API",
    description="RAG-powered chatbot in the style of Neil deGrasse Tyson",
    version="0.2.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fallback middleware: inject CORS headers if for any reason CORSMiddleware omitted them.
@app.middleware("http")
async def ensure_cors_headers(request, call_next):
    response = await call_next(request)
    origin = request.headers.get("origin")
    if origin and origin in cors_origins:
        # If CORSMiddleware failed to attach headers (observed missing Access-Control-Allow-Origin), add them.
        if "access-control-allow-origin" not in {k.lower(): v for k, v in response.headers.items()}:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Mount routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(sources.router, prefix="/api", tags=["sources"])
app.include_router(debug.router, prefix="/api", tags=["debug"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NDT Bot API",
        "version": "0.1.0",
        "docs": "/docs",
    }
