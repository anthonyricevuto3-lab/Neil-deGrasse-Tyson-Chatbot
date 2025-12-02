"""Chat endpoint with RAG pipeline."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

from backend.models.schemas import ChatRequest, ChatResponse
from backend.rag.pipelines import rag_pipeline
from backend.services.guardrails import check_scope
from backend.services.llm import generate_response
from backend.llm.provider import generate_chat
from backend.services.telemetry import log_request

router = APIRouter()


@router.options("/chat")
async def chat_options():
    """Handle CORS preflight for /chat."""
    # FastAPI/Starlette CORSMiddleware will attach the proper CORS headers.
    return JSONResponse(status_code=204, content=None)


@router.get("/chat")
async def chat_get_help():
    """Helper for accidental GET requests to /chat.

    Returns guidance on how to use the POST /chat endpoint.
    """
    return JSONResponse(
        {
            "detail": "Use POST /api/chat with JSON body {'message': '<your question>'}",
            "example": {"message": "What is a neutron star?"},
            "schema": {"message": "string"},
        }
    )

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

        # Generate response using provider abstraction (Claude Haiku 4.5 by default)
        # Combine user message with retrieved context
        prompt = f"Use the context to answer.\n\nContext:\n{context}\n\nQuestion: {request.message}"
        answer_text = generate_chat([
            {"role": "user", "content": prompt}
        ], max_tokens=800)

        response = {
            "answer": answer_text,
            "sources": [],
            "metadata": {"provider": "model"}
        }

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
