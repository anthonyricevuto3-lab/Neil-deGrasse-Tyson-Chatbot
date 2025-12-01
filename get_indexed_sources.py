"""Extract successfully indexed sources from vector store."""

from pathlib import Path
from backend.rag.store import load_store
from backend.settings import get_settings

def get_indexed_sources() -> list[str]:
    """Extract unique source URLs from the FAISS vector store."""
    settings = get_settings()
    store = load_store(Path(settings.vector_store_path))
    if store is None:
        print("No vector store found")
        return []
    
    sources: set[str] = set()
    try:
        for doc in store.docstore._dict.values():
            src = doc.metadata.get("source") if hasattr(doc, "metadata") else None
            if isinstance(src, str) and (src.startswith("http://") or src.startswith("https://")):
                sources.add(src)
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    return sorted(sources)

if __name__ == "__main__":
    sources = get_indexed_sources()
    print(f"Found {len(sources)} indexed sources:\n")
    for src in sources:
        print(src)
