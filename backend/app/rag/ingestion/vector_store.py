import os
import time
import uuid
import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

class CustomHTTPEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_url: str, timeout: int = 300):
        self.api_url = api_url
        self.timeout = timeout  # 5 phút — model 270M cần thời gian encode

    def __call__(self, input: Documents) -> Embeddings:
        n = len(input)
        print(f"[Embedding] Đang encode {n} chunks... (có thể mất vài phút với model 270M)")
        t0 = time.time()
        response = requests.post(
            self.api_url,
            json={"texts": input},
            timeout=self.timeout  # tránh bị timeout khi encode nhiều chunks
        )
        response.raise_for_status()
        elapsed = time.time() - t0
        print(f"[Embedding] ✅ Hoàn thành {n} chunks trong {elapsed:.1f}s ({elapsed/n:.2f}s/chunk)")
        return response.json()["embeddings"]

class ChromaManager:
    """
    Quản lý việc lưu trữ các Document Chunks vào ChromaDB.
    """
    def __init__(self, persist_directory="./.chroma", collection_name="disaster_knowledge"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Khởi tạo client: Sử dụng HttpClient nếu có CHROMA_HOST khác localhost (trong Docker Compose)
        chroma_host = os.environ.get("CHROMA_HOST", "localhost")
        chroma_port = int(os.environ.get("CHROMA_PORT", "8000"))
        
        if chroma_host and chroma_host != "localhost":
            print(f"[ChromaDB] Kết nối tới ChromaDB server qua HTTP tại {chroma_host}:{chroma_port}...")
            self.client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        else:
            print(f"[ChromaDB] Khởi tạo PersistentClient tại thư mục {self.persist_directory}...")
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Sử dụng microservice cho embedding
        default_embed = "http://embedding_service:8002/embed" if (chroma_host and chroma_host != "localhost") else "http://localhost:8002/embed"
        embedding_url = os.environ.get("EMBEDDING_SERVICE_URL", default_embed)
        self.embedding_fn = CustomHTTPEmbeddingFunction(api_url=embedding_url)
        
        # Tạo hoặc lấy collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, docs):
        """
        Nhận vào danh sách các Document (từ langchain text splitter) và lưu vào ChromaDB.
        """
        if not docs:
            return

        documents = []
        metadatas = []
        ids = []

        for i, doc in enumerate(docs):
            documents.append(doc.page_content)
            metadatas.append(doc.metadata if doc.metadata else {"source": "unknown"})
            # Dùng UUID4 để đảm bảo ID luôn unique, tránh overwrite khi loop nhanh
            ids.append(str(uuid.uuid4()))

        # Thêm vào collection — embedding được gọi 1 lần duy nhất cho toàn bộ batch
        print(f"[ChromaDB] Bắt đầu lưu {len(docs)} chunks...")
        t_start = time.time()
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        t_total = time.time() - t_start
        print(f"[ChromaDB] ✅ Đã lưu {len(docs)} chunks vào '{self.collection_name}' trong {t_total:.1f}s")

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
