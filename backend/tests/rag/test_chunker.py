from app.rag.ingestion.chunker import SemanticChunker

def test_semantic_chunker_empty():
    chunker = SemanticChunker()
    assert chunker.chunk_text("") == []
    assert chunker.chunk_text("   ") == []

def test_semantic_chunker_headers():
    markdown_text = """# Giới thiệu
Đây là phần giới thiệu.

## Chi tiết
Đây là chi tiết. Đoạn này cũng khá ngắn.

### Cảnh báo
Cần chú ý an toàn!
"""
    chunker = SemanticChunker(chunk_size=100, chunk_overlap=10)
    docs = chunker.chunk_text(markdown_text)
    
    assert len(docs) == 3
    assert "Header 1" in docs[0].metadata
    assert docs[0].metadata["Header 1"] == "Giới thiệu"
    assert "Header 2" in docs[1].metadata
    assert docs[1].metadata["Header 2"] == "Chi tiết"

def test_semantic_chunker_long_text():
    markdown_text = "# Lịch sử\n" + ("A " * 600)  # > 1000 chars
    chunker = SemanticChunker(chunk_size=500, chunk_overlap=50)
    docs = chunker.chunk_text(markdown_text)
    
    # Do text dài hơn 1000 char và chunk_size=500 nên nó phải cắt ra thành nhiều đoạn
    assert len(docs) >= 2
    # Metadata Header 1 phải được kế thừa sang tất cả các đoạn con
    assert all(doc.metadata.get("Header 1") == "Lịch sử" for doc in docs)
