from app.rag.retrieval.hybrid_search import HybridSearcher
from app.rag.retrieval.reranker import Reranker
from app.rag.ingestion.vector_store import ChromaManager

class KnowledgeAgent:
    """
    Agent chuyên phụ trách tra cứu thông tin từ Cẩm nang phòng chống thiên tai.
    Sử dụng kiến trúc Advanced RAG: Semantic Search với ChromaDB.
    """
    def __init__(self, chroma_manager: ChromaManager = None, reranker: Reranker = None):
        self.chroma_manager = chroma_manager or ChromaManager()
        self.reranker = reranker

    def answer_query(self, query: str) -> dict:
        """
        Xử lý câu hỏi bằng kiến thức nội bộ (Cẩm nang).
        """
        try:
            # 1. Retrieval (Semantic Search from ChromaDB)
            results = self.chroma_manager.search(query, n_results=5)
            
            retrieved_docs = []
            if results and "documents" in results and results["documents"]:
                docs = results["documents"][0]
                metadatas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else []
                for i, text in enumerate(docs):
                    retrieved_docs.append({
                        "text": text,
                        "metadata": metadatas[i] if i < len(metadatas) else {}
                    })
            
            if not retrieved_docs:
                return {"answer": "Không tìm thấy thông tin liên quan trong cẩm nang.", "sources": []}

            # 2. Reranking (optional)
            final_docs = retrieved_docs[:3]

            # 3. Tổng hợp câu trả lời
            context_str = "\n".join([doc["text"] for doc in final_docs])
            
            return {
                "answer": f"Dựa trên cẩm nang, đây là thông tin tôi tìm được:\n{context_str}",
                "sources": [doc.get("text", "")[:150] + "..." for doc in final_docs]
            }
        except Exception as e:
            print(f"Error querying Knowledge Base: {e}")
            return {"answer": "Đã có lỗi xảy ra khi truy xuất cơ sở dữ liệu.", "sources": []}

