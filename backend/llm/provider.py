from typing import List, Dict

from backend.settings import get_settings

try:
    from anthropic import Anthropic
except Exception:
    Anthropic = None  # type: ignore

try:
    from openai import OpenAI  # OpenAI Python SDK v1.x
except Exception:
    OpenAI = None  # type: ignore


def generate_chat(messages: List[Dict[str, str]], max_tokens: int = 1024) -> str:
    settings = get_settings()
    provider = settings.model_provider.lower()
    model = settings.llm_model

    if provider == "anthropic" and Anthropic is not None and settings.anthropic_api_key:
        client = Anthropic(api_key=settings.anthropic_api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
        )
        # Anthropic returns content array; concatenate text parts
        parts = []
        for blk in getattr(resp, "content", []) or []:
            txt = getattr(blk, "text", None)
            if isinstance(txt, str):
                parts.append(txt)
        return "\n".join(parts) if parts else str(resp)

    if provider == "openai" and OpenAI is not None and settings.openai_api_key:
        client = OpenAI(api_key=settings.openai_api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            temperature=settings.temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content or ""

    # Fallback: return simple string if neither provider configured
    return "Model provider not configured or SDK missing."
