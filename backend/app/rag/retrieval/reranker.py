class Reranker:
    """
    Sử dụng Cross-Encoder để Re-rank kết quả trả về từ Hybrid Search.
    Giúp đẩy các kết quả có ý nghĩa ngữ cảnh cao nhất lên đầu tiên.
    """
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", mock: bool = False):
        self.model_name = model_name
        self.mock = mock
        self.model = None
        
        if not self.mock:
            try:
                from sentence_transformers import CrossEncoder
                self.model = CrossEncoder(model_name)
            except ImportError:
                raise ImportError("Vui lòng cài đặt sentence-transformers để dùng tính năng này.")

    def rerank(self, query: str, documents: list[dict], top_k: int = 3) -> list[dict]:
        """
        Thực hiện tính điểm rerank cho các tài liệu.
        Lưu ý: documents là một danh sách các dict chứa key 'text'
        """
        if not documents:
            return []

        # Chuẩn bị input format cho CrossEncoder: list of (query, doc_text)
        cross_inp = [[query, doc["text"]] for doc in documents]
        
        # Lấy scores
        scores = self.model.predict(cross_inp)
        
        # Gắn scores vào documents
        for idx, doc in enumerate(documents):
            doc["cross_encoder_score"] = float(scores[idx])

        # Sắp xếp lại theo score
        reranked_docs = sorted(documents, key=lambda x: x["cross_encoder_score"], reverse=True)
        
        return reranked_docs[:top_k]
