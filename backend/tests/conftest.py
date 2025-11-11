"""Test fixtures and shared utilities."""

import pytest


@pytest.fixture
def sample_question():
    """Sample question for testing."""
    return "What is dark matter?"


@pytest.fixture
def sample_context():
    """Sample context with citations."""
    return """[Source: Astrophysics for People in a Hurry]
Dark matter is invisible matter that makes up most of the universe's mass.
It doesn't emit light but affects gravity.

[Source: Death by Black Hole]
We know dark matter exists because of its gravitational effects on galaxies."""


@pytest.fixture
def sample_documents():
    """Sample retrieved documents."""
    return [
        {
            "content": "Dark matter is invisible matter.",
            "source": "Astrophysics for People in a Hurry",
            "score": 0.95,
            "metadata": {},
        },
        {
            "content": "Dark matter affects gravity.",
            "source": "Death by Black Hole",
            "score": 0.88,
            "metadata": {},
        },
    ]
