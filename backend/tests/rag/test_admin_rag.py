import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.api.deps import get_current_admin_user

client = TestClient(app)

# Mock admin user dependency
def override_get_current_admin_user():
    return {"id": 1, "email": "admin@terraalert.com", "role": "ADMIN"}

app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user

@patch("app.api.admin_rag_router.master_parser.route_and_parse")
@patch("app.api.admin_rag_router.chunker.chunk_text")
def test_dry_run_ingestion(mock_chunk_text, mock_route_and_parse):
    # Setup mock
    mock_route_and_parse.return_value = "# Test Header\nThis is a test content."
    
    class MockDoc:
        def __init__(self, page_content, metadata):
            self.page_content = page_content
            self.metadata = metadata
            
    mock_chunk_text.return_value = [
        MockDoc("This is a test content.", {"Header 1": "Test Header"})
    ]

    # Create dummy file
    test_file_path = "test_upload.txt"
    with open(test_file_path, "w") as f:
        f.write("test content")
        
    try:
        with open(test_file_path, "rb") as f:
            response = client.post(
                "/api/v1/admin/rag/dry-run",
                files={"file": ("test_upload.txt", f, "text/plain")}
            )
            
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["text"] == "This is a test content."
        assert data[0]["metadata"]["Header 1"] == "Test Header"
    finally:
        os.remove(test_file_path)

@patch("app.api.admin_rag_router.chroma_manager.add_documents")
def test_commit_ingestion(mock_add_documents):
    payload = {
        "chunks": [
            {
                "text": "This is a chunk",
                "metadata": {"source": "test"}
            }
        ]
    }
    response = client.post(
        "/api/v1/admin/rag/commit",
        json=payload
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["inserted"] == 1
    mock_add_documents.assert_called_once()
