"""Sources endpoint returning training and indexed sources."""

from pathlib import Path
from fastapi import APIRouter, Query

from backend.rag.store import load_store
from backend.settings import get_settings

router = APIRouter()

@router.options("/sources")
async def sources_options():
    """Handle CORS preflight for /sources."""
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=204, content=None)


def _load_training_urls() -> list[str]:
    """Parse the training_urls.txt file collecting all HTTP/HTTPS lines.

    Ignores comments (# ...) and blank lines.
    """
    root = Path(__file__).resolve().parents[2]
    training_file = root / "data" / "urls" / "training_urls.txt"
    if not training_file.exists():
        return []
    urls: list[str] = []
    for line in training_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("http://") or line.startswith("https://"):
            urls.append(line)
    return urls


def _load_vector_store_sources() -> list[str]:
    """Extract unique source URLs from the FAISS vector store if present."""
    settings = get_settings()
    store = load_store(Path(settings.vector_store_path))
    if store is None:
        return []
    sources: set[str] = set()
    # langchain FAISS store keeps documents in docstore._dict
    try:
        for doc in store.docstore._dict.values():  # type: ignore[attr-defined]
            src = doc.metadata.get("source") if hasattr(doc, "metadata") else None
            if isinstance(src, str) and (src.startswith("http://") or src.startswith("https://")):
                sources.add(src)
    except Exception as e:  # pragma: no cover - defensive
        print(f"Error extracting sources from vector store: {e}")
    return sorted(sources)


@router.get("/sources")
async def sources_endpoint(indexed_only: bool = Query(False, description="If true, return only indexed vector store sources")) -> dict:
    """Return combined list of training URLs and indexed vector store sources.

    Response shape:
        {"sources": ["https://...", ...], "counts": {"training": X, "indexed": Y, "combined": Z}}
    """
    training = _load_training_urls()
    indexed = _load_vector_store_sources()
    if indexed_only:
        return {
            "sources": indexed,
            "counts": {"training": len(training), "indexed": len(indexed), "combined": len(indexed)},
        }
    combined = list(dict.fromkeys(training + indexed))  # preserve order, remove duplicates
    return {
        "sources": combined,
        "counts": {
            "training": len(training),
            "indexed": len(indexed),
            "combined": len(combined),
        },
    }
