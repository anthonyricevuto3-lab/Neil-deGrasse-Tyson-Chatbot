"""Test chat API endpoint."""

import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_chat_endpoint_success():
    """Test successful chat request."""
    response = client.post(
        "/api/chat",
        json={"message": "What is dark matter?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)


def test_chat_endpoint_empty_message():
    """Test chat with empty message."""
    response = client.post(
        "/api/chat",
        json={"message": ""}
    )
    
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_out_of_scope():
    """Test chat with out-of-scope question."""
    response = client.post(
        "/api/chat",
        json={"message": "Who should I vote for?"}
    )
    
    # May return 400 or answer depending on guardrail
    assert response.status_code in [200, 400]


def test_health_endpoints():
    """Test health check endpoints."""
    response = client.get("/api/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    response = client.get("/api/ready")
    assert response.status_code == 200
