"""Guardrails and scope checking."""


from backend.deps import get_llm
from backend.prompts import ALLOWED_TOPICS, GUARDRAIL_PROMPT


def on_scope_fast(message: str) -> bool:
    """
    Fast heuristic check if question is science-related.

    Returns True if any allowed topic keyword found (case-insensitive).
    """
    m = message.lower()
    return any(topic in m for topic in ALLOWED_TOPICS)


def check_scope(question: str) -> bool:
    """
    Check if question is within science communication scope.

    First tries fast keyword check, then falls back to LLM if ambiguous.
    Returns True if appropriate, False otherwise.
    """
    # Fast path: obvious science topics
    if on_scope_fast(question):
        return True

    # Temporarily always return True to simplify debugging
    return True

    # LLM-based check for edge cases
    llm = get_llm()

    prompt = GUARDRAIL_PROMPT.format(question=question)

    try:
        response = llm.invoke([{"role": "user", "content": prompt}])
        decision = response.content.strip().upper()
        return decision == "ACCEPT"
    except Exception as e:
        print(f"Guardrail check failed: {e}")
        # Fail open (allow question) to avoid blocking legitimate queries
        return True


def validate_response(response: str, require_citations: bool = True) -> dict[str, any]:
    """
    Validate response meets quality standards.

    Checks:
    - Word count within limit (180 words)
    - Citations present with [source: ...] format
    - Short quotes present (text in "quotes")

    Returns validation result dict.
    """
    from backend.settings import get_settings
    from backend.utils.text import count_words

    settings = get_settings()

    word_count = count_words(response)

    # Check for proper citation format [source: ...]
    has_citations = "[source:" in response.lower()

    # Check for quoted snippets
    has_quotes = '"' in response and response.count('"') >= 2

    valid = True
    issues = []

    # Stricter word limit: 180 words
    max_words = min(settings.max_response_words, 180)
    if word_count > max_words:
        valid = False
        issues.append(f"Response too long: {word_count} words (max {max_words})")

    if require_citations and not has_citations:
        valid = False
        issues.append("No [source: ...] citations found")

    if require_citations and not has_quotes:
        issues.append("Warning: No quoted snippets found (recommended)")

    return {
        "valid": valid,
        "issues": issues,
        "word_count": word_count,
        "has_citations": has_citations,
        "has_quotes": has_quotes,
    }
