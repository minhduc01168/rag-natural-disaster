# Bản Yêu Cầu Hệ Thống (System Requirements Document - SRD)
**Dự án:** TerraAlert - Nền tảng cảnh báo sớm sạt lở đất ứng dụng Agentic RAG và Dữ liệu vệ tinh.
*(Bản cập nhật kiến trúc theo nguyên tắc Phân tách Không gian & Thời gian)*

---

## 1. Xác Thực Nguồn Dữ Liệu Công Cộng & Miễn Phí

Để phục vụ nghiên cứu học thuật không có kinh phí, toàn bộ dữ liệu đầu vào được chuyển dịch sang các nguồn mở quốc tế được công nhận bởi cộng đồng khoa học:

* **Dữ liệu lượng mưa:** 
  * *Lịch sử:* Dữ liệu vệ tinh **NASA GPM IMERG** (Global Precipitation Measurement) hoặc **CHIRPS** tích hợp sẵn trên Google Earth Engine (GEE). Đạt độ phân giải không gian cao, miễn phí hoàn toàn cho nghiên cứu.
  * *Thời gian thực (Real-time):* **Meteostat API** hoặc **OpenWeatherMap (Free Tier)**. Cung cấp dữ liệu mưa theo giờ của các trạm khí tượng quốc tế tại Việt Nam.
* **Dữ liệu đặc tính địa chất & địa hình:**
  * *Độ dốc/Độ cao:* **SRTM DEM (Shuttle Radar Topography Mission)** độ phân giải 30m của NASA/USGS trên GEE.
  * *Thảm thực vật:* Vệ tinh **Sentinel-2 (ESA)** để tính toán chỉ số thực vật thời gian thực.
* **Dữ liệu lịch sử thiên tai (Ground Truth):**
  * **HDX (Humanitarian Data Exchange)** của UN OCHA và dữ liệu **DesInventar Sendai (UNDRR)**. Cung cấp file dạng hình học (Shapefile/GeoJSON) và tọa độ các vụ lũ quét, sạt lở lịch sử tại Việt Nam.

---

## 2. Tổng Quan Dự Án & Hàm Lượng Nghiên Cứu (Research Focus)

* **Tên đề tài nghiên cứu dự kiến:** *A Cost-Effective Multi-Agent Early Warning System for Landslides in Mountainous Regions Using Open Satellite Remote Sensing and Integrated RAG Architecture.*
* **Khu vực nghiên cứu thử nghiệm (Case Study):** Một tỉnh vùng cao trọng điểm (ví dụ: tỉnh Gia Lai hoặc khu vực Tây Nguyên/Tây Bắc).
* **Đóng góp khoa học & Triết lý thiết kế:**
  1. **Decoupled Architecture (Kiến trúc phân tách):** Giải quyết mâu thuẫn giữa độ trễ của AI và tính cấp bách của cứu nạn bằng cách phân tách hệ thống thành 2 luồng: **Fast Lane** (Cứu nạn thời gian thực) và **Slow Lane** (Học thuật, AI phân tích).
  2. Xây dựng bản đồ nhạy cảm sạt lở đất (LSM) từ dữ liệu vệ tinh mở (SRTM, Sentinel-2, GPM).
  3. Đề xuất kiến trúc **Multi-Agent RAG** giúp dịch lý thuyết khí tượng phức tạp thành khuyến nghị hành động ngôn ngữ tự nhiên.

---

## 3. Quy Trình Xử Lý Dữ Liệu Và Kiến Trúc Hệ Thống (Phân Tách Luồng)

Hệ thống được chia làm hai luồng (Lanes) xử lý độc lập để đảm bảo an toàn sinh mạng đồng thời giữ nguyên giá trị nghiên cứu AI:

1. **Slow Lane (Data Ingestion, ML Pipeline & AI RAG):**
   * *Background Workers (Celery + Redis):* Định kỳ trích xuất dữ liệu không gian từ GEE (SRTM DEM, Sentinel-2 NDVI, NASA GPM). Dữ liệu bản đồ nặng được lưu và truy vấn qua **PostgreSQL + PostGIS**.
   * *Gán nhãn & Huấn luyện Mô hình ML (Research Core):*
     * Chồng ghép tọa độ các vụ sạt lở lịch sử từ **HDX** lên bản đồ địa hình SRTM để tạo bộ dữ liệu có nhãn (labeled dataset).
     * Trích xuất các đặc trưng (features): độ dốc, độ cao (SRTM), chỉ số NDVI $= \frac{NIR - Red}{NIR + Red}$ (Sentinel-2), lượng mưa tích lũy (NASA GPM).
     * Huấn luyện thuật toán **Random Forest** (hoặc Frequency Ratio) để phân tích trọng số rủi ro từng yếu tố.
     * Xuất kết quả dưới dạng **Bản đồ Nhạy cảm Sạt lở (Landslide Susceptibility Map - LSM)** dạng GeoJSON/GeoTIFF, lưu vào PostGIS phục vụ Research Dashboard và Geographic Agent.
   * *Knowledge Base:* Các tài liệu phòng chống thiên tai được chunking và lưu trong **ChromaDB** phục vụ riêng cho các tác vụ RAG của TerraBot.
2. **Fast Lane (Real-time Alert & SOS Pipeline):**
   * *Alert API:* Gọi API từ Meteostat 3 giờ/lần. Nếu vượt ngưỡng bão hòa, kích hoạt Push Notification ngay lập tức thông qua luồng Basic REST/WebSockets. Không có sự can thiệp của AI RAG ở luồng này để đảm bảo độ trễ < 1 giây.

---

## 4. Yêu Cầu Chức Năng Chi Tiết (Khung "Trước - Trong - Sau" Thảm Họa)

### PHA 1: TRƯỚC VÀ SAU THẢM HỌA (Luồng Chậm - Showcase AI & Nghiên cứu)
*Phục vụ cán bộ quản lý, người dân chuẩn bị kỹ năng, và minh chứng học thuật.*

* **Màn hình 1: Research Dashboard (Bản đồ Nhạy cảm & Dữ liệu Vệ tinh)**
  * *Mục đích:* Trực quan hóa kết quả tính toán dữ liệu GIS.
  * *Tính năng:* Hiển thị bản đồ tương tác GeoJSON về nguy cơ sạt lở. Đánh dấu điểm thiên tai lịch sử (HDX). Biểu đồ Time-series lượng mưa tích lũy.
* **Màn hình 2: Không gian TerraBot (Kiến trúc Multi-Agent RAG)**
  * *Mục đích:* Giao diện chatbot hỏi đáp kỹ năng chuẩn bị trước bão/sạt lở và thống kê sau thảm họa.
  * *Kiến trúc:* Gồm 4 agents (Weather Agent, Geographic Agent, Knowledge Agent, Synthesis Agent).
  * *Ví dụ ngữ cảnh an toàn:* *"Bão sắp đổ bộ, nhà tôi ở vùng sườn đồi thì cần gia cố thế nào?"* -> TerraBot phân tích dữ liệu và tư vấn bằng ngôn ngữ tự nhiên.

### PHA 2: TRONG THẢM HỌA (Luồng Nhanh - Sinh tồn tức thời)
*Tối giản, không có độ trễ AI, tập trung vào cứu nạn thực tế.*

* **Màn hình 3: Home & Emergency Dashboard (Trang chủ & SOS)**
  * *Mục đích:* Báo cáo trạng thái rủi ro tức thời và cứu nạn.
  * *Tính năng:* Giao diện tối giản. Định vị tự động và báo rủi ro (Xanh/Vàng/Đỏ). Nút SOS khổng lồ, bấm để gửi tọa độ khẩn cấp.
* **Màn hình 4: Alert Center (Trung tâm Điều phối Cảnh báo)**
  * *Mục đích:* Phân loại rủi ro (Rule-based) và báo động Push Notification.
  * *Tính năng:* Cảnh báo màu theo ngưỡng: An toàn (Xanh), Cảnh giác (Vàng - Mưa vượt ngưỡng), Nguy hiểm (Đỏ - Mưa cực đoan).
* **Màn hình 5: Cẩm nang sinh tồn số (Digital Survival Guide)**
  * *Mục đích:* Cung cấp kiến thức sơ cứu, thoát hiểm khi mất Internet.
  * *Tính năng:* Danh mục hướng dẫn trực quan bằng hình ảnh/icon. Hoạt động offline hoàn toàn.

---

## 5. Yêu Cầu Phi Chức Năng & Công Nghệ Triển Khai

* **Bộ công nghệ (Tech Stack):**
  * *Frontend:* ReactJS / TailwindCSS. Bắt buộc thiết kế theo kiến trúc **PWA (Progressive Web App)** với Service Workers và IndexedDB để đảm bảo tính năng "Offline Survival Guide" luôn hoạt động khi sập mạng.
  * *Backend Fast Lane:* FastAPI, WebSockets/FCM cho Push Notifications.
  * *Backend Slow Lane:* Celery + Redis cho Data Ingestion; PostgreSQL + PostGIS cho dữ liệu không gian.
  * *Machine Learning (LSM):* **Scikit-learn** (Random Forest), `geopandas`, `shapely` cho xử lý và huấn luyện mô hình dự báo sạt lở. Google Earth Engine Python API để truy cập dữ liệu vệ tinh.
  * *AI Framework:* LangChain/LlamaIndex. Vector DB: ChromaDB. LLM API: Groq/Gemini Flash.
* **Hiệu năng & Vận hành (SLA):**
  * *SOS & Alert:* Độ trễ < 1 giây.
  * *TerraBot RAG:* Độ trễ < 5-10 giây (chỉ dùng trước/sau thảm họa).
  * *ML Model Training:* Chạy offline/batch trên Google Colab hoặc local, sau đó lưu model đã huấn luyện (`.pkl`) vào hệ thống.
  * Toàn bộ mã nguồn đóng gói bằng **Docker** để dễ triển khai.