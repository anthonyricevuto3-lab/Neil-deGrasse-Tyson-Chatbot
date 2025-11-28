"""Dense retrieval with FAISS."""

from pathlib import Path

from backend.rag.store import load_store
from backend.settings import get_settings
from backend.deps import get_embeddings


async def retrieve_documents(query: str, top_k: int | None = None) -> list[dict]:
    """
    Retrieve top-k documents for a query.

    Retrieves more documents than needed for downstream reranking.
    Default: 12 documents retrieved (optimized from 20 for faster performance),
    then reranker picks best 5.
    """
    settings = get_settings()
    # Reduced from 20 to 12 for better performance (still enough for reranking)
    k = top_k if top_k else 12

    # Load vector store (now cached globally)
    store = load_store(Path(settings.vector_store_path))
    if store is None:
        print("[retriever] No vector store available after load attempt.")
        return []

    # Basic embedding/index dimension sanity check to surface issues early
    try:
        test_vec = get_embeddings().embed_query("dimension-check")
        index_dim = getattr(store.index, "d", None)
        if index_dim is not None and len(test_vec) != index_dim:
            print(f"[retriever] Dimension mismatch: embed={len(test_vec)} index={index_dim}")
    except Exception as e:
        print(f"[retriever] Embedding dimension check failed: {e}")

    # Search
    try:
        results = store.similarity_search_with_score(query, k=k)
    except Exception as e:
        print(f"[retriever] similarity_search_with_score failed: {e}")
        return []

    documents = []
    for doc, score in results:
        documents.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "score": float(score),
                "metadata": doc.metadata,
            }
        )

    return documents
