"""Search/retrieval-only endpoint."""


from fastapi import APIRouter

from backend.models.schemas import SearchRequest, SearchResult
from backend.rag.retriever import retrieve_documents

router = APIRouter()


@router.post("/search", response_model=list[SearchResult])
async def search_endpoint(request: SearchRequest) -> list[SearchResult]:
    """
    Retrieve relevant documents without generating a response.
    Useful for testing retrieval quality.
    """
    documents = await retrieve_documents(
        query=request.query,
        top_k=request.top_k or 10,
    )

    return [
        SearchResult(
            content=doc["content"],
            source=doc["source"],
            score=doc["score"],
            metadata=doc.get("metadata", {}),
        )
        for doc in documents
    ]
