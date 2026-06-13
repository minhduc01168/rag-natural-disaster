# Bản Yêu Cầu Hệ Thống (System Requirements Document - SRD)
**Dự án:** TerraAlert - Nền tảng Hỗ trợ ra quyết định ứng phó sạt lở đất ứng dụng Advanced Agentic RAG.
*(Bản cập nhật kiến trúc loại bỏ ML, tập trung chuyên sâu vào Agentic RAG)*

---

## 1. Xác Thực Nguồn Dữ Liệu Công Cộng & Miễn Phí

Để phục vụ nghiên cứu học thuật không có kinh phí, toàn bộ dữ liệu đầu vào được chuyển dịch sang các nguồn mở quốc tế được công nhận bởi cộng đồng khoa học:

* **Dữ liệu lượng mưa:** 
  * *Lịch sử:* Dữ liệu vệ tinh **NASA GPM IMERG** (Global Precipitation Measurement) hoặc **CHIRPS** tích hợp sẵn trên Google Earth Engine (GEE). Đạt độ phân giải không gian cao, miễn phí hoàn toàn cho nghiên cứu.
  * *Thời gian thực (Real-time):* **Open-Meteo API** (Hoàn toàn mở, không giới hạn phi thương mại). Cung cấp dữ liệu mưa theo giờ của các trạm khí tượng quốc tế tại Việt Nam.
* **Dữ liệu đặc tính địa chất & địa hình:**
  * *Độ dốc/Độ cao:* **SRTM DEM (Shuttle Radar Topography Mission)** độ phân giải 30m của NASA/USGS trên GEE.
  * *Thảm thực vật:* Vệ tinh **Sentinel-2 (ESA)** để tính toán chỉ số thực vật thời gian thực.
* **Dữ liệu lịch sử thiên tai (Ground Truth):**
  * **HDX (Humanitarian Data Exchange)** của UN OCHA và dữ liệu **DesInventar Sendai (UNDRR)**. Cung cấp file dạng hình học (Shapefile/GeoJSON) và tọa độ các vụ lũ quét, sạt lở lịch sử tại Việt Nam.

---

## 2. Tổng Quan Dự Án & Hàm Lượng Nghiên Cứu (Research Focus)

* **Tên đề tài nghiên cứu dự kiến:** *An Intelligent Multi-Agent RAG System for Emergency Decision Support in Landslide Disasters.*
* **Khu vực nghiên cứu thử nghiệm (Case Study):** Các tỉnh vùng cao trọng điểm (ví dụ: khu vực Tây Nguyên/Tây Bắc, Việt Nam).
* **Đóng góp khoa học & Triết lý thiết kế:**
  1. **Decoupled Architecture (Kiến trúc phân tách):** Giải quyết mâu thuẫn giữa độ trễ của AI và tính cấp bách của cứu nạn bằng cách phân tách hệ thống thành 2 luồng: **Fast Lane** (Cứu nạn thời gian thực) và **Slow Lane** (Học thuật, Agentic RAG hỗ trợ ra quyết định).
  2. **Advanced RAG Pipeline:** Xây dựng hệ thống RAG chuyên sâu ứng dụng Semantic Chunking, Hybrid Search và mô hình Cross-Encoder để Re-ranking tài liệu cứu hộ.
  3. **Multi-Agent Orchestration:** Đề xuất kiến trúc đa tác vụ (Multi-Agent) kết hợp LLM và khả năng gọi API bên ngoài (Thời tiết, Địa hình) để tự động hóa việc đưa ra khuyến nghị sơ tán và sinh tồn.
  4. **Rigorous Evaluation:** Đánh giá định lượng chất lượng của hệ thống RAG bằng framework RAGAS (Faithfulness, Answer Relevance, Context Precision).

---

## 3. Quy Trình Xử Lý Dữ Liệu Và Kiến Trúc Hệ Thống (Phân Tách Luồng)

Hệ thống được chia làm hai luồng (Lanes) xử lý độc lập để đảm bảo an toàn sinh mạng đồng thời giữ nguyên giá trị nghiên cứu AI:

1. **Slow Lane (Advanced Agentic RAG - Research Core):**
   * *Data Ingestion (Chế biến tài liệu):* Thu thập cẩm nang phòng chống thiên tai, luật đê điều, hướng dẫn sơ tán (PDF, Word). Áp dụng **Semantic Chunking** để chia nhỏ tài liệu theo ngữ nghĩa thay vì độ dài cố định.
   * *Vector Database & Retrieval:* Embedding tài liệu lưu vào **ChromaDB/Pinecone**. Triển khai cơ chế **Hybrid Search** (kết hợp BM25 và Vector Search) và sử dụng Cross-Encoder để **Re-ranking** các tài liệu phù hợp nhất.
   * *Multi-Agent Orchestration:* 
     * `Router Agent`: Phân loại ý định người dùng (hỏi luật, hỏi thời tiết, hay cần hướng dẫn sơ tán).
     * `Retrieval Agent`: Chuyên truy xuất VectorDB để tìm quy trình chuẩn.
     * `Tool Agents`: Chuyên gọi API bên ngoài (Open-Meteo lấy lượng mưa, OpenTopoData lấy độ cao/địa hình).
     * `Synthesis Agent`: Trích xuất thông tin từ các Agent khác để viết câu trả lời hoàn chỉnh, trung thực (Faithful) và dễ hiểu.
   * *RAG Evaluation:* Hệ thống được benchmark liên tục bằng **RAGAS/TruLens** để đo lường độ chính xác và giảm thiểu ảo giác (Hallucination).
2. **Fast Lane (Real-time Alert & SOS Pipeline):**
   * *Alert API:* Gọi API từ Open-Meteo 3 giờ/lần. Nếu vượt ngưỡng bão hòa, kích hoạt Push Notification ngay lập tức thông qua luồng Basic REST/WebSockets. Không có sự can thiệp của AI RAG ở luồng này để đảm bảo độ trễ < 1 giây.

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
  * *Backend Slow Lane (Agentic RAG):* FastAPI, Celery + Redis cho Data Ingestion tài liệu lớn.
  * *Advanced RAG & Evaluation:* LangChain/LlamaIndex. Vector DB: ChromaDB hoặc Pinecone. Đánh giá tự động: **RAGAS**, TruLens. LLM API: Groq/Gemini Flash.
* **Hiệu năng & Vận hành (SLA):**
  * *SOS & Alert:* Độ trễ < 1 giây.
  * *Multi-Agent RAG:* Độ trễ < 5-10 giây. Tối ưu hóa bằng cơ chế streaming response.
  * Toàn bộ mã nguồn đóng gói bằng **Docker** để dễ triển khai.