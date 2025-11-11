"""Dense retrieval with FAISS."""

from pathlib import Path
from typing import List

from backend.rag.store import load_store
from backend.settings import get_settings


async def retrieve_documents(query: str, top_k: int | None = None) -> List[dict]:
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
    
    # Search
    results = store.similarity_search_with_score(query, k=k)
    
    documents = []
    for doc, score in results:
        documents.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "Unknown"),
            "score": float(score),
            "metadata": doc.metadata,
        })
    
    return documents
