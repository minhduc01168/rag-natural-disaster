from rank_bm25 import BM25Okapi

class HybridSearcher:
    """
    Kết hợp kết quả tìm kiếm của Vector Search (Semantic) và Keyword Search (BM25).
    """
    def __init__(self, documents: list[str]):
        """
        Khởi tạo BM25 index từ một list of documents.
        """
        self.documents = documents
        # Tokenize cơ bản cho tiếng Việt (tách theo khoảng trắng)
        tokenized_corpus = [doc.lower().split(" ") for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def keyword_search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Tìm kiếm BM25.
        Trả về danh sách dict chứa text và score.
        """
        tokenized_query = query.lower().split(" ")
        scores = self.bm25.get_scores(tokenized_query)
        
        # Sắp xếp top_k
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for i in top_n:
            if scores[i] > 0:  # Chỉ lấy kết quả có score > 0
                results.append({
                    "text": self.documents[i],
                    "score": scores[i],
                    "method": "bm25"
                })
        return results

    def rrf_fusion(self, bm25_results: list[dict], vector_results: list[dict], k: int = 60) -> list[dict]:
        """
        Thuật toán Reciprocal Rank Fusion (RRF)
        Hợp nhất kết quả từ BM25 và Vector Search.
        """
        # Khởi tạo dict để lưu RRF score cho từng text
        rrf_scores = {}
        
        # Hàm helper xử lý list
        def add_to_rrf(results_list, weight=1.0):
            for rank, item in enumerate(results_list):
                text = item["text"]
                if text not in rrf_scores:
                    rrf_scores[text] = 0.0
                rrf_scores[text] += weight * (1.0 / (k + rank + 1))

        add_to_rrf(bm25_results)
        add_to_rrf(vector_results)

        # Sắp xếp theo score
        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [{"text": text, "rrf_score": score} for text, score in sorted_results]
