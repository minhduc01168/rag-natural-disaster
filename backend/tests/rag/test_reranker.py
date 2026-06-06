import pytest
from app.rag.retrieval.reranker import Reranker

def test_reranker_success():
    reranker = Reranker(model_name="test-model", mock=True)
    
    # Fake the model object
    class FakeModel:
        def predict(self, inp):
            # Return fixed scores based on order
            return [0.1, 0.9]
    reranker.model = FakeModel()
    
    query = "Làm sao để an toàn khi có bão?"
    documents = [
        {"text": "Đoạn 1 nói về không liên quan."},
        {"text": "Đoạn 2 nói về việc ở trong nhà kiên cố khi bão đến."}
    ]
    
    results = reranker.rerank(query, documents, top_k=2)
    
    # Đoạn 2 có score cao hơn (0.9 vs 0.1) nên phải lên đầu tiên
    assert len(results) == 2
    assert results[0]["text"] == "Đoạn 2 nói về việc ở trong nhà kiên cố khi bão đến."
    assert results[0]["cross_encoder_score"] == 0.9
    assert results[1]["text"] == "Đoạn 1 nói về không liên quan."
    assert results[1]["cross_encoder_score"] == 0.1

def test_reranker_empty():
    reranker = Reranker(model_name="test-model", mock=True)
    results = reranker.rerank("bão", [])
    assert results == []
