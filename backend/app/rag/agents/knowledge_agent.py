from app.rag.retrieval.hybrid_search import HybridSearcher
from app.rag.retrieval.reranker import Reranker

class KnowledgeAgent:
    """
    Agent chuyên phụ trách tra cứu thông tin từ Cẩm nang phòng chống thiên tai.
    Sử dụng kiến trúc Advanced RAG: Hybrid Search + Cross-Encoder Reranking.
    """
    def __init__(self, searcher: HybridSearcher = None, reranker: Reranker = None):
        self.searcher = searcher
        self.reranker = reranker

    def answer_query(self, query: str) -> dict:
        """
        Xử lý câu hỏi bằng kiến thức nội bộ (Cẩm nang).
        """
        if not self.searcher:
            # Fallback for testing/mocking
            return {"answer": "Bạn cần phải cẩn thận khi có thiên tai.", "sources": []}
            
        # 1. Retrieval (Hybrid Search)
        # Vì đây là ví dụ, giả định ta chỉ gọi keyword_search (BM25) và mock vector search
        # Trong thực tế, vector_search kết nối với ChromaDB sẽ được inject vào đây
        retrieved_docs = self.searcher.keyword_search(query, top_k=5)
        
        if not retrieved_docs:
            return {"answer": "Không tìm thấy thông tin trong cẩm nang.", "sources": []}

        # 2. Reranking
        if self.reranker:
            final_docs = self.reranker.rerank(query, retrieved_docs, top_k=3)
        else:
            final_docs = retrieved_docs[:3]

        # 3. Tổng hợp câu trả lời (Trong thực tế sẽ đưa final_docs vào LLM Prompt)
        # Giả lập trả về context raw
        context_str = "\n".join([doc["text"] for doc in final_docs])
        
        return {
            "answer": f"Dựa trên cẩm nang, đây là thông tin tôi tìm được:\n{context_str}",
            "sources": [doc.get("text", "") for doc in final_docs]
        }
