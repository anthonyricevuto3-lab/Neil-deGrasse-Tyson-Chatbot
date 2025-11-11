"""LLM generation service."""

from typing import AsyncIterator, Dict

from backend.deps import get_llm
from backend.prompts import RESPONSE_TEMPLATE, SYSTEM_PROMPT
from backend.settings import get_settings


async def generate_response(
    question: str,
    context: str,
    stream: bool = False,
) -> Dict[str, any] | AsyncIterator[str]:
    """
    Generate response using LLM.
    
    Args:
        question: User question
        context: Retrieved context
        stream: Whether to stream response
    
    Returns:
        Dict with answer and sources, or stream of chunks
    """
    llm = get_llm()
    settings = get_settings()
    
    # Format prompt
    prompt = RESPONSE_TEMPLATE.format(
        context=context,
        question=question,
    )
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    
    if stream:
        # Streaming response
        async def stream_chunks():
            async for chunk in llm.astream(messages):
                if chunk.content:
                    yield chunk.content
        
        return stream_chunks()
    else:
        # Complete response
        response = await llm.ainvoke(messages)
        
        # Extract sources from context
        sources = []
        for line in context.split("\n"):
            if line.startswith("[Source:"):
                source = line.replace("[Source:", "").replace("]", "").strip()
                if source not in sources:
                    sources.append(source)
        
        return {
            "answer": response.content,
            "sources": sources,
            "metadata": {
                "model": settings.llm_model,
                "temperature": settings.temperature,
            }
        }
