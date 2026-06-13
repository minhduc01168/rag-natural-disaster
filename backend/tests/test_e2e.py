import pytest
import requests

BACKEND_URL = "http://localhost:8000/api/v1"
EMBEDDING_URL = "http://localhost:8001"

def test_embedding_service_health():
    """Kiểm tra dịch vụ Embedding có đang hoạt động và load model không"""
    try:
        response = requests.get(f"{EMBEDDING_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        assert data.get("model_loaded") is True
    except requests.exceptions.ConnectionError:
        pytest.skip("Embedding service is not running.")

def test_embedding_generation():
    """Kiểm tra việc tạo embedding vector từ text"""
    try:
        payload = {"texts": ["Cảnh báo sạt lở đất tại khu vực đồi núi"]}
        response = requests.post(f"{EMBEDDING_URL}/embed", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "embeddings" in data
        assert len(data["embeddings"]) == 1
        assert len(data["embeddings"][0]) > 0
    except requests.exceptions.ConnectionError:
        pytest.skip("Embedding service is not running.")

def test_backend_rag_chat_e2e():
    """Kiểm tra luồng RAG Chat (Slow Lane)"""
    try:
        payload = {"query": "Dấu hiệu nhận biết sạt lở đất là gì?"}
        response = requests.post(f"{BACKEND_URL}/rag/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend is not running.")
