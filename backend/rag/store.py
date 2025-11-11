"""FAISS vector store management with caching for performance."""

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS

from backend.deps import get_embeddings

# Global cache for vector store (avoid reloading on every request)
_vector_store_cache = None


def load_store(store_path: Path, use_cache: bool = True) -> FAISS:
    """
    Load existing FAISS store with caching.
    
    Args:
        store_path: Path to vector store
        use_cache: Use cached store (default True for performance)
    
    Returns:
        FAISS vector store
    """
    global _vector_store_cache
    
    # Return cached store if available
    if use_cache and _vector_store_cache is not None:
        return _vector_store_cache
    
    embeddings = get_embeddings()
    try:
        # Try with the parameter first (newer langchain versions)
        store = FAISS.load_local(
            str(store_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    except TypeError:
        # Fall back to without parameter (older versions)
        store = FAISS.load_local(
            str(store_path),
            embeddings,
        )
    
    # Cache for future requests
    if use_cache:
        _vector_store_cache = store
    
    return store


def add_to_store(chunks: List[dict], store_path: Path) -> None:
    """Add chunks to vector store (creates if doesn't exist)."""
    store_path.mkdir(parents=True, exist_ok=True)
    embeddings = get_embeddings()
    
    texts = [chunk["content"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            **chunk.get("metadata", {}),
        }
        for chunk in chunks
    ]
    
    if (store_path / "index.faiss").exists():
        # Load existing and add
        store = load_store(store_path)
        store.add_texts(texts, metadatas=metadatas)
    else:
        # Create new
        store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    
    # Save
    store.save_local(str(store_path))
