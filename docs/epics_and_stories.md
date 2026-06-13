# Danh Sách Các Epics (Project Backlog - Advanced RAG Edition)

Dự án **TerraAlert** được chia thành 7 Epics chính để triển khai cuốn chiếu. Việc chia nhỏ nhằm ưu tiên xử lý luồng cảnh báo sinh tồn trước (Fast Lane), sau đó ráp hệ thống Agentic RAG phức tạp (Slow Lane).

## Epic 1: Project Setup & Foundation
- **Story 1.1:** Khởi tạo PWA scaffolding (React + TailwindCSS).
- **Story 1.2:** Khởi tạo FastAPI backend template (tách folder structure: `fast_lane` và `slow_lane`).
- **Story 1.3:** Thiết lập Docker & Docker Compose cho toàn bộ hệ thống (PostgreSQL, Redis, ChromaDB, Web, Worker).

## Epic 2: Fast Lane Core (Real-time SOS & Alerts)
- **Story 2.1:** Tích hợp Open-Meteo API lấy dữ liệu thời tiết realtime.
- **Story 2.2:** Xây dựng Rule-based engine trên FastAPI để phân loại cảnh báo (An toàn, Cảnh giác, Nguy hiểm).
- **Story 2.3:** Cài đặt hệ thống gửi thông báo Push Notifications (WebSockets hoặc FCM).
- **Story 2.4:** Xây dựng giao diện màn hình *Home & Emergency Dashboard*.
- **Story 2.5:** Xây dựng giao diện màn hình *Alert Center*.

## Epic 3: Offline Survival Guide (PWA Resilience)
- **Story 3.1:** Thiết kế và xây dựng giao diện *Cẩm nang sinh tồn số* bằng hình ảnh/icon tối ưu.
- **Story 3.2:** Cài đặt Service Workers và IndexedDB để lưu trữ (cache) nội dung tĩnh.
- **Story 3.3:** Viết test giả lập (simulate) trạng thái mất mạng và xác nhận luồng offline hoạt động trơn tru.

## Epic 4: Knowledge Base Construction & Ingestion
- **Story 4.1:** Thu thập, số hóa và làm sạch tài liệu: Cẩm nang phòng chống thiên tai, luật đê điều, hướng dẫn sơ tán sạt lở (PDF, Word).
- **Story 4.2:** Tích hợp Document Parser (vd: `unstructured`) để trích xuất text từ PDF, đảm bảo giữ nguyên bảng biểu và cấu trúc văn bản.
- **Story 4.3:** Xây dựng thuật toán **Semantic Chunking** thay vì cắt theo độ dài, giúp giữ trọn vẹn ngữ nghĩa từng đoạn văn bản.
- **Story 4.4:** Áp dụng Embedding model và lưu toàn bộ chunks vào Vector Database (ChromaDB / Pinecone).

## Epic 5: Advanced RAG Core & Retrieval
- **Story 5.1:** Xây dựng cơ chế **Hybrid Search**: Kết hợp tìm kiếm từ khóa (BM25) và tìm kiếm ngữ nghĩa (Vector Search).
- **Story 5.2:** Triển khai **Cross-Encoder Re-ranking**: Xếp hạng lại top các chunks tìm được để đảm bảo lấy ra những thông tin chính xác nhất.
- **Story 5.3:** Cài đặt framework đánh giá **RAGAS** hoặc TruLens. Viết kịch bản test để tự động chấm điểm độ chính xác (Faithfulness) và độ liên quan (Answer Relevance).

## Epic 6: Multi-Agent Orchestration (TerraBot)
- **Story 6.1:** Khởi tạo các API Tools: `get_weather_now`, `get_elevation`.
- **Story 6.2:** Xây dựng các Agents: `RouterAgent` (điều hướng), `KnowledgeAgent` (gọi RAG Core ở Epic 5), `ToolAgent` (gọi API thời tiết/địa hình).
- **Story 6.3:** Xây dựng `SynthesisAgent` để tổng hợp thông tin, đưa ra quyết định sơ tán theo ngôn ngữ tự nhiên.
- **Story 6.4:** Tích hợp LLM API (Gemini Flash/Groq) và xây dựng giao diện chat *TerraBot Space* trên Frontend.

## Epic 7: Research Dashboard (Geo-Spatial Visualization)
- **Story 7.1:** Xây dựng API query dữ liệu không gian từ PostGIS.
- **Story 7.2:** Tích hợp bản đồ tương tác (Leaflet) vào React Frontend.
- **Story 7.3:** Trực quan hóa dữ liệu thời tiết (lượng mưa) và vị trí cảnh báo rủi ro lên bản đồ thay vì hiển thị dữ liệu ML.
