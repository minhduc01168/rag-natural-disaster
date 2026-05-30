# Danh Sách Các Epics (Project Backlog)

Dự án **TerraAlert** được chia thành 6 Epics chính để triển khai cuốn chiếu. Việc chia nhỏ nhằm ưu tiên xử lý luồng cảnh báo sinh tồn trước (Fast Lane), sau đó mới ráp hệ thống AI phức tạp (Slow Lane).

## Epic 1: Project Setup & Foundation
- **Story 1.1:** Khởi tạo PWA scaffolding (React + TailwindCSS).
- **Story 1.2:** Khởi tạo FastAPI backend template (tách folder structure: `fast_lane` và `slow_lane`).
- **Story 1.3:** Thiết lập Docker & Docker Compose cho toàn bộ hệ thống (PostgreSQL, Redis, ChromaDB, Web, Worker).

## Epic 2: Fast Lane Core (Real-time SOS & Alerts)
- **Story 2.1:** Tích hợp Meteostat API lấy dữ liệu thời tiết realtime.
- **Story 2.2:** Xây dựng Rule-based engine trên FastAPI để phân loại cảnh báo (An toàn, Cảnh giác, Nguy hiểm).
- **Story 2.3:** Cài đặt hệ thống gửi thông báo Push Notifications (WebSockets hoặc FCM).
- **Story 2.4:** Xây dựng giao diện màn hình *Home & Emergency Dashboard*.
- **Story 2.5:** Xây dựng giao diện màn hình *Alert Center*.

## Epic 3: Offline Survival Guide (PWA Resilience)
- **Story 3.1:** Thiết kế và xây dựng giao diện *Cẩm nang sinh tồn số* bằng hình ảnh/icon tối ưu.
- **Story 3.2:** Cài đặt Service Workers và IndexedDB để lưu trữ (cache) nội dung tĩnh.
- **Story 3.3:** Viết test giả lập (simulate) trạng thái mất mạng và xác nhận luồng offline hoạt động trơn tru.

## Epic 4: Slow Lane Data Ingestion & ML Pipeline
- **Story 4.1:** Thiết lập Celery Workers và Redis cho job queue.
- **Story 4.2:** Viết cron job gọi API từ Google Earth Engine (SRTM, Sentinel-2, GPM) và dữ liệu HDX.
- **Story 4.3:** Xây dựng script chuẩn hóa dữ liệu GIS và lưu trữ vào PostgreSQL (có cài extension PostGIS).
- **Story 4.4:** Huấn luyện mô hình Machine Learning (Random Forest) dựa trên dữ liệu GIS và lịch sử HDX để tạo bản đồ nhạy cảm sạt lở (LSM).

## Epic 5: Multi-Agent RAG System (TerraBot)
- **Story 5.1:** Thiết lập ChromaDB và nhúng (embed) các tài liệu phòng chống thiên tai để làm Knowledge Base.
- **Story 5.2:** Khởi tạo 4 Agents bằng LangChain/LlamaIndex (Weather, Geographic, Knowledge, Synthesis).
- **Story 5.3:** Tích hợp LLM API (Gemini/Groq) để Agents diễn dịch ngôn ngữ tự nhiên tiếng Việt.
- **Story 5.4:** Xây dựng giao diện chat *TerraBot Space* và API endpoint tương ứng.

## Epic 6: Research Dashboard (GIS Visualization)
- **Story 6.1:** Xây dựng API (REST) để query dữ liệu GeoJSON/không gian từ PostGIS.
- **Story 6.2:** Tích hợp thư viện bản đồ tương tác (Leaflet hoặc Mapbox) vào React.
- **Story 6.3:** Trực quan hóa bản đồ nhạy cảm sạt lở (LSM) sinh ra từ mô hình ML và các biểu đồ Time-series lượng mưa.
