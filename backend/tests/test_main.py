import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# ==================== System Tests ====================

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["status"] == "running"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ==================== RAG Tests ====================

def test_chat():
    response = client.post(
        "/api/v1/rag/chat",
        json={"query": "Xin chào"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "route_taken" in data
    assert "sources" in data

def test_chat_empty_query():
    response = client.post(
        "/api/v1/rag/chat",
        json={"query": "   "},
    )
    assert response.status_code == 400
