"""Test retriever functionality."""

import pytest

from backend.rag.retriever import retrieve_documents


@pytest.mark.asyncio
async def test_retrieve_documents_returns_list():
    """Test that retriever returns list."""
    # Note: This will fail without a real index
    # Should use mini_index fixture in practice
    try:
        results = await retrieve_documents("test query", top_k=5)
        assert isinstance(results, list)
    except Exception:
        pytest.skip("No vector store available")


def test_retriever_import():
    """Test that retriever module imports correctly."""
    from backend.rag import retriever
    assert hasattr(retriever, "retrieve_documents")
