from app.rag.retrieval.hybrid_search import HybridSearcher
from app.rag.retrieval.reranker import Reranker
from app.rag.ingestion.vector_store import ChromaManager

class KnowledgeAgent:
    """
    Agent chuyên phụ trách tra cứu thông tin từ Cẩm nang phòng chống thiên tai.
    Sử dụng kiến trúc Advanced RAG: Semantic Search với ChromaDB + BM25 + Reranking.
    """
    def __init__(self, chroma_manager: ChromaManager = None, use_reranker: bool = True):
        self.chroma_manager = chroma_manager or ChromaManager()
        
        # Lấy toàn bộ văn bản để xây dựng tập BM25 (chạy ngầm trong RAM)
        all_data = self.chroma_manager.get_all_documents()
        documents = all_data.get("documents", []) if all_data else []
        self.hybrid_searcher = HybridSearcher(documents) if documents else None
        
        # Khởi tạo Reranker (nếu dùng)
        self.reranker = Reranker(mock=False) if use_reranker else None

    def answer_query(self, query: str) -> dict:
        """
        Xử lý câu hỏi bằng kiến thức nội bộ (Advanced RAG).
        """
        try:
            # 1. Semantic Search (Vector) từ ChromaDB
            results = self.chroma_manager.search(query, n_results=10)
            vector_docs = []
            if results and "documents" in results and results["documents"]:
                for doc in results["documents"][0]:
                    vector_docs.append({"text": doc})

            # 2. Keyword Search (BM25)
            bm25_docs = []
            if self.hybrid_searcher:
                bm25_docs = self.hybrid_searcher.keyword_search(query, top_k=10)

            # Nếu cả 2 đều rỗng thì báo lỗi
            if not vector_docs and not bm25_docs:
                return {"answer": "Không tìm thấy thông tin liên quan trong cẩm nang.", "sources": []}

            # 3. Reciprocal Rank Fusion (RRF)
            if self.hybrid_searcher:
                fused_docs = self.hybrid_searcher.rrf_fusion(bm25_docs, vector_docs)
            else:
                fused_docs = vector_docs

            # 4. Reranking bằng Cross-Encoder
            if self.reranker and fused_docs:
                final_docs = self.reranker.rerank(query, fused_docs, top_k=3)
            else:
                final_docs = fused_docs[:3]

            # 5. Tổng hợp câu trả lời
            context_str = "\n".join([doc["text"] for doc in final_docs])
            
            return {
                "answer": f"Dựa trên cẩm nang, đây là thông tin tôi tìm được:\n{context_str}",
                "sources": [doc.get("text", "")[:150] + "..." for doc in final_docs]
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error querying Knowledge Base: {e}")
            return {"answer": "Đã có lỗi xảy ra khi truy xuất cơ sở dữ liệu.", "sources": []}


