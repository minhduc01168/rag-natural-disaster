import os
import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

class CustomHTTPEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_url: str):
        self.api_url = api_url

    def __call__(self, input: Documents) -> Embeddings:
        response = requests.post(self.api_url, json={"texts": input})
        response.raise_for_status()
        return response.json()["embeddings"]

class ChromaManager:
    """
    Quản lý việc lưu trữ các Document Chunks vào ChromaDB.
    """
    def __init__(self, persist_directory="./.chroma", collection_name="disaster_knowledge"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Khởi tạo PersistentClient để lưu dữ liệu xuống đĩa cứng
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Sử dụng microservice cho embedding
        # URL trỏ tới container embedding_service trong mạng docker (hoặc localhost nếu chạy local)
        embedding_url = os.environ.get("EMBEDDING_SERVICE_URL", "http://embedding_service:8002/embed")
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
            # Tạo ID duy nhất dựa trên index hoặc nội dung
            ids.append(f"doc_{time.time()}_{i}")

        # Thêm vào collection (Sẽ tự động sử dụng model microsoft/harrier-oss-v1-0.6b đã cấu hình)
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Đã lưu {len(docs)} chunks vào ChromaDB (collection: {self.collection_name})")

    def search(self, query: str, n_results: int = 3):
        """
        Tìm kiếm semantic cơ bản.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
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

import time
