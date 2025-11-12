"""Cross-encoder reranking with BGE."""

import importlib.util

from backend.settings import get_settings

# Don't import FlagEmbedding at module level - only when actually using it
RERANKER_AVAILABLE = None

# Lazy load reranker
_reranker = None


def _check_reranker_available():
    """Check if FlagEmbedding is available (cached)."""
    global RERANKER_AVAILABLE
    if RERANKER_AVAILABLE is None:
        RERANKER_AVAILABLE = importlib.util.find_spec("FlagEmbedding") is not None
        if not RERANKER_AVAILABLE:
            print(
                "⚠️  FlagEmbedding not available. Using simple similarity fallback for reranking."
            )
    return RERANKER_AVAILABLE


def get_reranker():
    """Get or create BGE reranker model (more accurate than MiniLM)."""
    if not _check_reranker_available():
        return None

    global _reranker
    if _reranker is None:
        from FlagEmbedding import FlagReranker

        _reranker = FlagReranker("BAAI/bge-reranker-large", use_fp16=True)
    return _reranker


async def rerank_documents(
    query: str,
    documents: list[dict],
    top_k: int | None = None,
) -> list[dict]:
    """Rerank documents using BGE cross-encoder (batch processing) or fallback."""
    settings = get_settings()
    k = top_k or settings.rerank_top_k

    if not documents:
        return []

    # Fallback: use existing similarity scores if reranker unavailable
    if not _check_reranker_available():
        # Documents already have similarity scores from retriever
        documents.sort(key=lambda x: x.get("score", 0), reverse=True)
        return documents[:k]

    # Prepare query-document pairs
    pairs = [[query, doc["content"]] for doc in documents]

    # Score with BGE reranker (increased batch size for better throughput)
    reranker = get_reranker()
    scores = reranker.compute_score(pairs, batch_size=32)

    # Handle single document case (scores is float, not list)
    if not isinstance(scores, list):
        scores = [scores]

    # Add scores and sort by relevance
    for doc, score in zip(documents, scores):
        doc["rerank_score"] = float(score)

    documents.sort(key=lambda x: x["rerank_score"], reverse=True)

    return documents[:k]
