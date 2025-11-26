"""FAISS vector store management with caching for performance."""

import os
from pathlib import Path
from urllib.request import urlretrieve

from langchain_community.vectorstores import FAISS

from backend.deps import get_embeddings

# Global cache for vector store (avoid reloading on every request)
_vector_store_cache = None

# Azure Blob Storage URLs for vector store files
BLOB_BASE_URL = "https://ndtchatbotstorage.blob.core.windows.net/vectorstore"
BLOB_SAS_TOKEN = "se=2025-12-03T06%3A57%3A07Z&sp=r&sv=2022-11-02&sr=c&sig=nEP3OCnGRIgVW9llRSPaPTNSOEzGVIrM5bgmePqTLQ4%3D"
VECTOR_STORE_FILES = ["index.faiss", "index.pkl"]


def _download_vector_store_from_blob(store_path: Path) -> bool:
    """Download vector store files from Azure Blob Storage if they don't exist locally."""
    store_path.mkdir(parents=True, exist_ok=True)
    
    try:
        for filename in VECTOR_STORE_FILES:
            local_file = store_path / filename
            if not local_file.exists():
                blob_url = f"{BLOB_BASE_URL}/{filename}?{BLOB_SAS_TOKEN}"
                print(f"Downloading {filename} from Azure Blob Storage...")
                urlretrieve(blob_url, local_file)
                print(f"Downloaded {filename} successfully")
        return True
    except Exception as e:
        print(f"Error downloading vector store from blob: {e}")
        return False


def load_store(store_path: Path, use_cache: bool = True) -> FAISS | None:
    """
    Load existing FAISS store with caching.

    Args:
        store_path: Path to vector store
        use_cache: Use cached store (default True for performance)

    Returns:
        FAISS vector store or None if not found
    """
    global _vector_store_cache

    # Return cached store if available
    if use_cache and _vector_store_cache is not None:
        return _vector_store_cache

    # Check if vector store exists, if not try to download from blob
    if not (store_path / "index.faiss").exists():
        print("Vector store not found locally, attempting to download from Azure Blob Storage...")
        if not _download_vector_store_from_blob(store_path):
            print("Failed to download vector store from blob storage")
            return None
        print("Vector store downloaded successfully from blob storage")

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
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None

    # Cache for future requests
    if use_cache:
        _vector_store_cache = store

    return store


def add_to_store(chunks: list[dict], store_path: Path) -> None:
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
