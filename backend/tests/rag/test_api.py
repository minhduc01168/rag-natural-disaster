from fastapi.testclient import TestClient
from app.api.rag_router import router, synthesis_agent
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_chat_endpoint_success():
    # Because we're using mock=True in synthesis_agent
    response = client.post("/chat", json={"query": "thời tiết hà nội"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "thời tiết hà nội"
    assert data["route_taken"] == "weather"
    assert "[MOCK_LLM_RESPONSE]" in data["answer"]
    assert "OpenWeatherMap API" in data["sources"]

def test_chat_endpoint_empty_query():
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Query cannot be empty"
