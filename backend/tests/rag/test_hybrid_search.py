from app.rag.retrieval.hybrid_search import HybridSearcher

def test_hybrid_searcher():
    documents = [
        "Sạt lở đất thường xảy ra ở vùng núi sau mưa lớn.",
        "Cách sơ cứu người bị đuối nước là hô hấp nhân tạo.",
        "Mưa lớn kéo dài gây ngập lụt ở đồng bằng."
    ]
    
    searcher = HybridSearcher(documents)
    
    # Test keyword search
    results = searcher.keyword_search("mưa lớn", top_k=2)
    assert len(results) == 2
    assert "mưa lớn" in results[0]["text"].lower()
    
    # Mocks cho RRF
    bm25_mock = [
        {"text": "Mưa lớn kéo dài gây ngập lụt ở đồng bằng.", "score": 1.5},
        {"text": "Sạt lở đất thường xảy ra ở vùng núi sau mưa lớn.", "score": 1.0}
    ]
    vector_mock = [
        {"text": "Sạt lở đất thường xảy ra ở vùng núi sau mưa lớn.", "score": 0.9},
        {"text": "Mưa lớn kéo dài gây ngập lụt ở đồng bằng.", "score": 0.8}
    ]
    
    # Test RRF
    rrf_results = searcher.rrf_fusion(bm25_mock, vector_mock)
    
    assert len(rrf_results) == 2
    # Vì "Sạt lở đất" rank 2 bên BM25 và rank 1 bên Vector
    # "Mưa lớn" rank 1 bên BM25 và rank 2 bên Vector
    # RRF score sẽ bằng nhau hoặc chênh lệch nhỏ, ta kiểm tra format trả về:
    assert "rrf_score" in rrf_results[0]
