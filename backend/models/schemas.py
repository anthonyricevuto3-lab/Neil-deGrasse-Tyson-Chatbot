"""Pydantic schemas for API requests and responses."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str
    sources: List[str]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchRequest(BaseModel):
    """Search request schema."""
    query: str = Field(..., min_length=1)
    top_k: int | None = Field(None, ge=1, le=50)


class SearchResult(BaseModel):
    """Search result schema."""
    content: str
    source: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
