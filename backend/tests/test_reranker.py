"""Test reranker functionality."""

import pytest

from backend.rag.rerank import rerank_documents


@pytest.mark.asyncio
async def test_rerank_documents(sample_documents):
    """Test reranking documents."""
    query = "What is dark matter?"
    
    reranked = await rerank_documents(query, sample_documents, top_k=2)
    
    assert isinstance(reranked, list)
    assert len(reranked) <= 2
    
    # Check that rerank scores are added
    if reranked:
        assert "rerank_score" in reranked[0]


@pytest.mark.asyncio
async def test_rerank_empty_documents():
    """Test reranking with empty list."""
    reranked = await rerank_documents("test", [], top_k=5)
    assert reranked == []
