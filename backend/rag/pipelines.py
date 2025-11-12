"""End-to-end RAG pipeline."""


from backend.rag.context import format_context
from backend.rag.rerank import rerank_documents
from backend.rag.retriever import retrieve_documents


async def rag_pipeline(query: str) -> str:
    """
    Complete RAG pipeline: retrieve → rerank → format.

    Returns formatted context string ready for LLM.
    """
    # 1. Retrieve
    documents = await retrieve_documents(query)

    if not documents:
        return "No relevant context found."

    # 2. Rerank
    reranked = await rerank_documents(query, documents)

    # 3. Format
    context = format_context(reranked)

    return context


async def rag_pipeline_with_sources(query: str) -> dict:
    """
    RAG pipeline that returns both context and sources.

    Returns:
        {
            "context": formatted context string,
            "documents": list of document dicts,
            "sources": list of unique source names
        }
    """
    # 1. Retrieve
    documents = await retrieve_documents(query)

    if not documents:
        return {
            "context": "No relevant context found.",
            "documents": [],
            "sources": [],
        }

    # 2. Rerank
    reranked = await rerank_documents(query, documents)

    # 3. Format
    context = format_context(reranked)
    sources = list(set(doc["source"] for doc in reranked))

    return {
        "context": context,
        "documents": reranked,
        "sources": sources,
    }
