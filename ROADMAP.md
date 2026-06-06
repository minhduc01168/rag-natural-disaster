# TerraAlert - Master Roadmap

Roadmap quản lý tiến độ tổng thể của dự án TerraAlert, đặc biệt là giai đoạn chuyển đổi sang hệ thống **Agentic RAG**.

## 📍 Phase 1: Ingestion & Vector Storage (Hoàn thành)
- `[x]` Thiết lập `Parser` hỗ trợ cắt nhỏ file PDF, Markdown theo kích thước (chunk size).
- `[x]` Tích hợp HuggingFace Embeddings để nhúng tiếng Việt.
- `[x]` Thiết lập ChromaDB `VectorStore` để lưu trữ dữ liệu cẩm nang sinh tồn offline và tài liệu sạt lở.
- `[x]` Xây dựng Test: Đảm bảo luồng Ingestion hoạt động ổn định.

## 📡 Phase 2: Advanced Retrieval & Re-ranking (Hoàn thành)
- `[x]` Triển khai `HybridSearch`: Kết hợp Vector Search (ChromaDB) và Keyword Search (BM25) để giải quyết tình trạng thiếu chính xác với các truy vấn ngắn.
- `[x]` Triển khai `Reranker`: Sử dụng mô hình Cross-Encoder để xếp hạng lại top-K kết quả từ tìm kiếm lai, tối ưu hóa mức độ liên quan.
- `[x]` Xây dựng Test: Xác minh hiệu năng Hybrid Search với Mock.

## 🤖 Phase 3: Multi-Agent Orchestration (Hoàn thành)
- `[x]` Triển khai cấu trúc thư mục Agents (`router`, `knowledge`, `synthesis`, `tools`).
- `[x]` Xây dựng `RouterAgent`: Quyết định điều hướng truy vấn (weather tool vs knowledge base).
- `[x]` Xây dựng `KnowledgeAgent`: Kết nối Pipeline RAG để lấy ngữ cảnh.
- `[x]` Xây dựng Test: Xác minh quá trình Routing dựa vào regex/mock-intent.

## 🧠 Phase 4: LLM Generation & Backend Wiring (Hoàn thành)
- `[x]` Thiết lập `LLMGenerator` dùng Google Gemini 1.5 với Prompt Engineering chặt chẽ (Tránh hallucinations).
- `[x]` Tích hợp `SynthesisAgent` làm nhạc trưởng điều phối các luồng Agent.
- `[x]` Xóa bỏ Router Machine Learning cũ, tạo `rag_router.py` chuyên biệt cho API `/rag/chat`.
- `[x]` Kiểm soát ngoại lệ và lỗi mạng (HTTPException).
- `[x]` Hoàn tất 100% Backend Unit Tests (16 passed).

## 🚀 Phase 5: Frontend Integration & Deployment (Hoàn thành)
- `[x]` Tích hợp API Chat vào UI TerraBot trên Frontend (`ChatWindow.tsx`).
- `[x]` Vô hiệu hóa `postgres` và `redis` trong Docker Compose để dồn tài nguyên cho ChromaDB và LLM.
- `[x]` Chạy E2E Build qua Docker Compose.
