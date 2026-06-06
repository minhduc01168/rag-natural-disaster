import os
import shutil
import pytest
from app.rag.ingestion.vector_store import ChromaManager

class DummyDoc:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

@pytest.fixture
def temp_chroma_dir(tmp_path):
    # Sử dụng tmp_path của pytest để tạo một thư mục .chroma tạm thời
    chroma_dir = str(tmp_path / ".chroma_test")
    yield chroma_dir
    # Dọn dẹp sau khi test
    if os.path.exists(chroma_dir):
        # Retry logic for Windows since ChromaDB might hold file locks
        try:
            shutil.rmtree(chroma_dir)
        except Exception:
            pass

def test_chroma_manager_add_and_search(temp_chroma_dir):
    manager = ChromaManager(persist_directory=temp_chroma_dir, collection_name="test_col")
    
    docs = [
        DummyDoc("Sạt lở đất thường xảy ra ở vùng núi sau mưa lớn.", {"source": "doc1", "Header 1": "Khái niệm"}),
        DummyDoc("Cách sơ cứu người bị đuối nước là hô hấp nhân tạo.", {"source": "doc2", "Header 1": "Sơ cứu"}),
    ]
    
    manager.add_documents(docs)
    
    # Test search
    results = manager.search("nguyên nhân sạt lở", n_results=1)
    
    # Results là một dict có chứa 'documents', 'metadatas', 'ids'
    assert results is not None
    assert "documents" in results
    assert len(results["documents"][0]) == 1
    
    # Phải match được câu sạt lở
    assert "Sạt lở đất" in results["documents"][0][0]
    
    # Metadata phải giữ được
    assert results["metadatas"][0][0]["Header 1"] == "Khái niệm"
