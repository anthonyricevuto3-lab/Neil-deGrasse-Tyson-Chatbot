"""Text utilities."""

import re


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def clip_to_word_limit(text: str, max_words: int) -> str:
    """Clip text to word limit."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


def extract_quotes(text: str) -> list[str]:
    """Extract quoted text from a string."""
    # Match text in quotes (single or double)
    pattern = r'["\']([^"\']+)["\']'
    matches = re.findall(pattern, text)
    return matches


def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace from text."""
    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)
    # Replace multiple newlines with double newline
    text = re.sub(r"\n\n+", "\n\n", text)
    return text.strip()
