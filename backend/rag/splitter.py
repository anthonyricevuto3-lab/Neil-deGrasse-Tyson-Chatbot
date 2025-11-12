"""Text splitter with attribution."""

from typing import Any

from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.settings import get_settings


def split_with_attribution(
    text: str,
    source: str,
    metadata: dict[str, Any] | None = None,
) -> list[dict]:
    """
    Split text into chunks with source attribution.

    Each chunk includes:
    - content: The text content
    - source: Source identifier
    - metadata: Additional metadata
    """
    settings = get_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)

    return [
        {
            "content": chunk,
            "source": source,
            "metadata": metadata or {},
        }
        for chunk in chunks
    ]
