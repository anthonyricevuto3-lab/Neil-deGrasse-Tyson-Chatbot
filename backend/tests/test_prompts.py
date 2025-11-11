"""Test prompts and templates."""

from backend.prompts import GUARDRAIL_PROMPT, RESPONSE_TEMPLATE, SYSTEM_PROMPT


def test_system_prompt_exists():
    """Test that system prompt is defined."""
    assert SYSTEM_PROMPT
    assert "Neil deGrasse Tyson" in SYSTEM_PROMPT
    assert len(SYSTEM_PROMPT) > 100


def test_response_template_has_placeholders():
    """Test that response template has required placeholders."""
    assert "{context}" in RESPONSE_TEMPLATE
    assert "{question}" in RESPONSE_TEMPLATE


def test_guardrail_prompt_has_placeholder():
    """Test that guardrail prompt has question placeholder."""
    assert "{question}" in GUARDRAIL_PROMPT


def test_prompts_formatting():
    """Test that prompts can be formatted."""
    formatted = RESPONSE_TEMPLATE.format(
        context="Test context",
        question="Test question"
    )
    assert "Test context" in formatted
    assert "Test question" in formatted
