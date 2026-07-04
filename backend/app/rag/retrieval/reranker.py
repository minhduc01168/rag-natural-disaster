import threading

class Reranker:
    """
    Sử dụng Cross-Encoder để Re-rank kết quả trả về từ Hybrid Search.
    Giúp đẩy các kết quả có ý nghĩa ngữ cảnh cao nhất lên đầu tiên.

    Eager-load tại startup (gọi preload() trong lifespan FastAPI).
    Thread-safe: dùng threading.Lock để tránh race condition.
    Graceful fallback: nếu load thất bại → passthrough (không crash server).
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", mock: bool = False):
        self.model_name = model_name
        self.mock = mock
        self.model = None
        self._ready = False
        self._lock = threading.Lock()

    def preload(self) -> bool:
        """
        Eager-load model — gọi từ FastAPI lifespan khi startup.
        Trả về True nếu load thành công, False nếu thất bại.
        """
        with self._lock:
            if self._ready:
                return True
            if self.mock:
                self._ready = True
                return True
            try:
                from sentence_transformers import CrossEncoder
                print(f"[Reranker] 🔄 Đang load model '{self.model_name}'...")
                self.model = CrossEncoder(self.model_name)
                self._ready = True
                print(f"[Reranker] ✅ Sẵn sàng — model '{self.model_name}' đã load thành công.")
                return True
            except Exception as e:
                print(f"[Reranker] ⚠️  Không thể load model '{self.model_name}': {e}")
                print("[Reranker]    → Chạy ở chế độ passthrough (không rerank).")
                self.model = None
                self._ready = True  # đánh dấu đã thử, không retry
                return False

    @property
    def is_ready(self) -> bool:
        return self._ready

    def rerank(self, query: str, documents: list[dict], top_k: int = 3) -> list[dict]:
        """
        Thực hiện tính điểm rerank cho các tài liệu.
        documents: danh sách dict chứa key 'text'.
        Nếu model chưa load hoặc thất bại → passthrough top_k.
        """
        if not documents:
            return []

        # Nếu mock hoặc model load thất bại → passthrough
        if self.mock or self.model is None:
            return documents[:top_k]

        try:
            cross_inp = [[query, doc["text"]] for doc in documents]
            scores = self.model.predict(cross_inp)

            for idx, doc in enumerate(documents):
                doc["cross_encoder_score"] = float(scores[idx])

            reranked = sorted(documents, key=lambda x: x["cross_encoder_score"], reverse=True)
            return reranked[:top_k]

        except Exception as e:
            print(f"[Reranker] ⚠️  Lỗi khi rerank: {e}. Trả về kết quả không reranked.")
            return documents[:top_k]
