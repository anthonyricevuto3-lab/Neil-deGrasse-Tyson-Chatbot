"""Context formatting for LLM prompts."""


def format_context(documents: list[dict]) -> str:
    """
    Format retrieved documents into context string with titles.

    Format includes both title and domain for better citations:
    [{title}]
    {content}
    [Source: {source}]
    """
    if not documents:
        return "No relevant context found."

    context_parts = []
    for doc in documents:
        source = doc.get("source", "Unknown")
        content = doc.get("content", "")

        # Extract title and domain from metadata
        metadata = doc.get("metadata", {})
        title = metadata.get("title", "")
        domain = metadata.get("domain", "")

        # Use title if available, otherwise domain or source
        display_title = title or domain or source.split("/")[2] if "/" in source else source

        # Format with title for cleaner citations
        context_parts.append(f"[{display_title}]\n{content}\n[Source: {source}]")

    return "\n\n".join(context_parts)


def extract_sources(documents: list[dict]) -> list[dict]:
    """
    Extract unique sources with titles from documents.

    Returns list of dicts with title, domain, and URL.
    """
    sources = {}
    for doc in documents:
        source = doc.get("source", "Unknown")
        metadata = doc.get("metadata", {})

        if source not in sources:
            sources[source] = {
                "title": metadata.get("title", ""),
                "domain": metadata.get("domain", ""),
                "url": source,
            }

    return list(sources.values())
