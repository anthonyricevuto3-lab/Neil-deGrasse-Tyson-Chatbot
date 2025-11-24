"""Chat endpoint with RAG pipeline."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.models.schemas import ChatRequest, ChatResponse
from backend.rag.pipelines import rag_pipeline
from backend.services.guardrails import check_scope
from backend.services.llm import generate_response
from backend.services.telemetry import log_request

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint with RAG pipeline.

    1. Check scope/guardrails
    2. Retrieve relevant context
    3. Generate response with LLM
    4. Validate and return
    """
    try:
        # Log request
        log_request("chat", {"message": request.message})

        # Check scope
        if not check_scope(request.message):
            raise HTTPException(
                status_code=400, detail="Question is outside NDT's scope (science/education only)"
            )

        # Run RAG pipeline
        context = await rag_pipeline(request.message)

        # Generate response
        response = await generate_response(
            question=request.message,
            context=context,
        )

        return ChatResponse(
            response=response["answer"],
            sources=response["sources"],
            metadata=response.get("metadata", {}),
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint (SSE)."""

    async def generate():
        # Check scope
        if not check_scope(request.message):
            yield "data: {'error': 'Out of scope'}\n\n"
            return

        # Run RAG pipeline
        context = await rag_pipeline(request.message)

        # Stream response
        async for chunk in generate_response(
            question=request.message,
            context=context,
            stream=True,
        ):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
