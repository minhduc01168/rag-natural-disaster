# TerraAlert - Master Roadmap

Roadmap quản lý tiến độ tổng thể của dự án TerraAlert. Cập nhật file này thường xuyên cùng với `aihub-execution-plan.md` và `sprint-status.yaml` mỗi khi có thay đổi trạng thái theo workflow `/update-plan`.

## 📍 Epic 1: Project Setup & Foundation
- [ ] Khởi tạo PWA scaffolding (React + TailwindCSS).
- [ ] Khởi tạo FastAPI backend template (`fast_lane`, `slow_lane`).
- [ ] Thiết lập Docker & Docker Compose (PostgreSQL, Redis, ChromaDB, Backend, Frontend).

## 🚑 Epic 2: Fast Lane Core (Real-time SOS & Alerts)
- [ ] Tích hợp Meteostat API lấy thời tiết realtime.
- [ ] Rule-based engine trên FastAPI phân loại cảnh báo (Xanh/Vàng/Đỏ).
- [ ] Gửi thông báo Push Notifications (WebSockets/FCM).
- [ ] Giao diện Home & Emergency Dashboard.
- [ ] Giao diện Alert Center.

## ⛺ Epic 3: Offline Survival Guide (PWA Resilience)
- [ ] Giao diện Cẩm nang sinh tồn số (UI offline-first).
- [ ] Cài đặt Service Workers và IndexedDB để cache content.
- [ ] Test giả lập mất mạng (offline mode).

## 📡 Epic 4: Slow Lane Data Ingestion & ML Pipeline
- [ ] Thiết lập Celery Workers và Redis.
- [ ] Viết cron job gọi GEE API (SRTM, Sentinel-2, GPM) & HDX.
- [ ] Script chuẩn hóa GIS vào PostgreSQL + PostGIS.
- [ ] Huấn luyện mô hình Machine Learning (Random Forest) tạo bản đồ nhạy cảm sạt lở (LSM).

## 🤖 Epic 5: Multi-Agent RAG System (TerraBot)
- [ ] Thiết lập ChromaDB và Knowledge Base.
- [ ] Khởi tạo 4 Agents bằng LangChain/LlamaIndex.
- [ ] Tích hợp LLM API (Gemini/Groq) tiếng Việt.
- [ ] Giao diện chat TerraBot Space & API.

## 🗺️ Epic 6: Research Dashboard (GIS Visualization)
- [ ] API query GeoJSON/không gian từ PostGIS.
- [ ] Tích hợp bản đồ Leaflet/Mapbox.
- [ ] Trực quan hóa bản đồ sạt lở (LSM) và biểu đồ Time-series.
