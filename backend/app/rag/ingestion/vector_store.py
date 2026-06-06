import os
import chromadb
from chromadb.config import Settings
import google.generativeai as genai

class ChromaManager:
    """
    Quản lý việc lưu trữ các Document Chunks vào ChromaDB.
    """
    def __init__(self, persist_directory="./.chroma", collection_name="disaster_knowledge"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Khởi tạo PersistentClient để lưu dữ liệu xuống đĩa cứng
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Tạo hoặc lấy collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

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

        # Thêm vào collection (ChromaDB sẽ tự động gọi default embedding function nếu không config embedding riêng)
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

import time
