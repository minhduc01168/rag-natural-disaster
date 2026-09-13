import os
import time
import uuid
import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

CHROMA_HOST = os.environ.get("CHROMA_HOST", "")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
PERSIST_DIRECTORY = os.environ.get("PERSIST_DIRECTORY", "./.chroma")
EMBEDDING_SERVICE_URL = os.environ.get("EMBEDDING_SERVICE_URL", "http://embedding_service:8002/embed" if CHROMA_HOST else "http://localhost:8002/embed")

class CustomHTTPEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_url: str, timeout: int = 600):
        self.api_url = api_url
        self.timeout = timeout

    def __call__(self, input: Documents) -> Embeddings:
        n = len(input)
        print(f"[Embedding] Đang encode {n} chunks...")
        t0 = time.time()
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    self.api_url,
                    json={"texts": input},
                    timeout=self.timeout
                )
                response.raise_for_status()
                elapsed = time.time() - t0
                print(f"[Embedding] ✅ Hoàn thành {n} chunks trong {elapsed:.1f}s ({elapsed/max(n,1):.2f}s/chunk)")
                return response.json()["embeddings"]
            except Exception as e:
                if attempt < max_retries:
                    print(f"[Embedding] ⚠️ Thử lại lần {attempt + 1} do lỗi: {e}")
                    time.sleep(2)
                else:
                    raise e

class ChromaManager:
    """
    Quản lý Vector Store ChromaDB.
    Mặc định kết nối tới ChromaDB server độc lập qua REST API (docker-compose: 'chromadb:8000').
    Hỗ trợ fallback sang chế độ local PersistentClient nếu không có host/port hoặc khi truyền persist_directory (unit test).
    Sử dụng model microsoft/harrier-oss-v1-0.6b (270M) qua custom HTTP embedding service.
    """
    def __init__(self, collection_name: str = "disaster_knowledge", persist_directory: str = None, **kwargs):
        self.collection_name = collection_name
        self.persist_directory = persist_directory or kwargs.get("persist_directory") or PERSIST_DIRECTORY
        self.embedding_fn = CustomHTTPEmbeddingFunction(api_url=EMBEDDING_SERVICE_URL)
        
        # Nếu có persist_directory riêng (unit test), khởi tạo PersistentClient độc lập
        if persist_directory or kwargs.get("persist_directory"):
            print(f"[ChromaDB] Khởi tạo PersistentClient tại thư mục {self.persist_directory}...")
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        elif CHROMA_HOST:
            print(f"[ChromaDB] Kết nối tới ChromaDB server qua HTTP tại {CHROMA_HOST}:{CHROMA_PORT}...")
            self.client = chromadb.HttpClient(
                host=CHROMA_HOST,
                port=CHROMA_PORT
            )
        else:
            # Fallback: Local PersistentClient (khi chạy test local không có docker)
            print(f"[ChromaDB] Fallback sang Local PersistentClient tại {self.persist_directory}...")
            self.client = chromadb.PersistentClient(path=self.persist_directory)

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, docs, batch_size: int = 4):
        """
        Nhận vào danh sách các Document và lưu vào ChromaDB theo từng batch nhỏ (mặc định 4).
        Giúp tránh timeout (>600s) khi gọi embedding service trên CPU và làm sạch metadata.
        """
        if not docs:
            return

        total = len(docs)
        print(f"[ChromaDB] Bắt đầu lưu {total} chunks (batch_size={batch_size})...")
        t_start = time.time()

        for start_idx in range(0, total, batch_size):
            end_idx = min(start_idx + batch_size, total)
            batch_docs = docs[start_idx:end_idx]

            batch_documents = []
            batch_metadatas = []
            batch_ids = []

            for doc in batch_docs:
                batch_documents.append(doc.page_content)

                # Làm sạch metadata: ChromaDB chỉ chấp nhận str, int, float, bool
                raw_meta = dict(doc.metadata) if doc.metadata else {}
                clean_meta = {}
                for k, v in raw_meta.items():
                    if v is None:
                        clean_meta[str(k)] = ""
                    elif isinstance(v, (str, int, float, bool)):
                        clean_meta[str(k)] = v
                    else:
                        clean_meta[str(k)] = str(v)

                if "source" not in clean_meta:
                    clean_meta["source"] = clean_meta.get("source_file", "unknown")

                batch_metadatas.append(clean_meta)
                batch_ids.append(str(uuid.uuid4()))

            batch_num = (start_idx // batch_size) + 1
            total_batches = (total + batch_size - 1) // batch_size
            print(f"[ChromaDB] 📦 Đang nạp batch {batch_num}/{total_batches} ({len(batch_documents)} chunks)...")

            self.collection.add(
                documents=batch_documents,
                metadatas=batch_metadatas,
                ids=batch_ids
            )

        t_total = time.time() - t_start
        print(f"[ChromaDB] ✅ Đã lưu thành công toàn bộ {total} chunks vào '{self.collection_name}' trong {t_total:.1f}s")

    def search(self, query: str, n_results: int = 3):
        """
        Tìm kiếm semantic cơ bản.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances'],
        )
        return results

    def get_all_documents(self):
        """
        Lấy toàn bộ documents từ collection để phục vụ BM25 indexing.
        """
        try:
            return self.collection.get()
        except Exception as e:
            print(f"Error fetching all documents: {e}")
            return {"documents": [], "metadatas": [], "ids": []}
