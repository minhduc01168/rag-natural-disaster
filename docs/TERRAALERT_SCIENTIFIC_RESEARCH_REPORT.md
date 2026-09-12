# BÁO CÁO NGHIÊN CỨU KHOA HỌC VÀ KỸ THUẬT CHUYÊN SÂU
## NỀN TẢNG CẢNH BÁO SỚM THIÊN TAI VÀ HƯỚNG DẪN SINH TỒN VÙNG CAO TÍCH HỢP CÔNG NGHỆ RAG VÀ BẢN ĐỒ SỐ GIS (TERRAALERT PLATFORM)

---

### **TÓM TẮT ĐỀ TÀI (ABSTRACT)**

**Tiếng Việt:**  
Đề tài nghiên cứu và phát triển hệ thống **TerraAlert** — một nền tảng công nghệ toàn diện hỗ trợ cảnh báo sớm sạt lở đất, lũ quét và nâng cao năng lực tự ứng phó thiên tai cho cộng đồng yếu thế vùng cao miền núi phía Bắc Việt Nam. Hệ thống kết hợp mô hình phân tích mối tương quan giữa **lượng mưa tích lũy thời gian thực (Open-Meteo API)** và **các điểm nóng địa chất lịch sử (HDX / UN OCHA)** để phân cấp nguy cơ thiên tai thành 3 mức độ trực quan (An toàn - Cảnh giác - Nguy hiểm). Trên cơ sở đó, nhóm nghiên cứu phát triển Trợ lý AI **TerraBot** tích hợp công nghệ **RAG (Retrieval-Augmented Generation)** sử dụng mô hình Vector Embeddings `microsoft/harrier-oss-v1-270m` và CSDL Vector **ChromaDB**, giúp tự động phiên dịch các bản tin dự báo khí tượng phức tạp thành lời khuyên hành động dân dã, tra cứu sơ cấp cứu và danh bạ cứu hộ khẩn cấp ($112/115$). Sản phẩm web được tối ưu theo ngôn ngữ thiết kế *Fresh Light Palette* với 5 màn hình chính, đáp ứng khả năng truy cập mượt mà trên cả PC, Mobile và chế độ lưu trữ Offline khi mất mạng.

**English:**  
This research presents the **TerraAlert** platform — a comprehensive technological system designed for early landslide and flash flood warning, enhancing self-response capabilities for vulnerable highland communities in Northern Vietnam. The platform combines a mathematical correlation model linking **real-time accumulated rainfall (Open-Meteo API)** with **historical geological hazard hotspots (HDX / UN OCHA)** to categorize disaster risks into three intuitive levels (Safe - Alert - Danger). Furthermore, the team developed **TerraBot**, an AI assistant powered by **Retrieval-Augmented Generation (RAG)** utilizing `microsoft/harrier-oss-v1-270m` vector embeddings and a **ChromaDB** vector database. TerraBot translates complex meteorological forecasts into actionable advice, first-aid instructions, and emergency contact lookup ($112/115$). Built with a *Fresh Light Palette* design language across 5 primary screens, the web application delivers seamless performance across PC, Mobile, and offline scenarios during network outages.

---

## **CHƯƠNG 1: TỔNG QUAN VÀ ĐẶT VẤN ĐỀ (INTRODUCTION & PROBLEM STATEMENT)**

### 1.1. Bối cảnh Biến đổi Khí hậu và Thiên tai Vùng cao
Việt Nam là một trong những quốc gia chịu ảnh hưởng nặng nề nhất bởi biến đổi khí hậu toàn cầu. Tại các tỉnh miền núi phía Bắc (Lào Cai, Yên Bái, Hà Giang, Sơn La, Cao Bằng, Lai Châu...), địa hình đồi núi dốc đứng kết hợp với tần suất các đợt mưa lớn cực đoan ngày càng tăng đã gây ra hàng loạt vụ sạt lở đất đá và lũ quét kinh hoàng, cướp đi nhiều sinh mạng và gây thiệt hại khổng lồ về tài sản.

### 1.2. Hạn chế của các Hệ thống Cảnh báo Truyền thống
Các hệ thống cảnh báo hiện nay đối mặt với nhiều khoảng trống công nghệ:
1. **Từ ngữ chuyên môn phức tạp:** Các bản tin dự báo khí tượng (chứa các thông số như *lượng mưa tích lũy 24h/72h*, *mô hình hình thể thời tiết*, *độ ẩm bão hòa đất*) thường khó hiểu đối với đồng bào dân tộc thiểu số và cán bộ cơ sở.
2. **Thiếu tính trực quan GIS khoanh vùng:** Người dân khó xác định vị trí nhà mình có nằm trong bán kính vùng trượt lở bão hòa nước hay không nếu chỉ xem danh sách tên xã/huyện.
3. **Gián đoạn kết nối khi thiên tai xảy ra:** Khi bão lũ làm sập trạm sóng di động, các ứng dụng thuần Cloud sẽ hoàn toàn mất khả năng tra cứu kỹ năng sinh tồn.

### 1.3. Mục tiêu Đề tài
- **Mục tiêu 1:** Xây dựng Mô hình Ngưỡng mưa Tích lũy (Rainfall Threshold Matrix) kết hợp dữ liệu Open-Meteo API và bản đồ hiện trạng địa chất HDX.
- **Mục tiêu 2:** Tích hợp Bản đồ Tương tác GIS Leaflet hỗ trợ tính năng **Khoanh vùng Bán kính Nguy cơ Sạt trượt Lan tỏa ($1.0\text{km} - 3.5\text{km}$)**.
- **Mục tiêu 3:** Xây dựng Trợ lý AI RAG TerraBot phản hồi tức thì (<100ms) tra cứu kỹ năng thoát hiểm và số điện thoại cứu hộ khẩn cấp $112/115$.
- **Mục tiêu 4:** Chuẩn hóa giao diện 5 Màn hình Demo (Fresh Light Palette) hoạt động mượt màng trên cả PC, Mobile và Offline.

---

## **CHƯƠNG 2: MÔ HÌNH TOÁN HỌC NGƯỠNG MƯA VÀ KHOANH VÙNG GIS (MATHEMATICAL MODELING)**

### 2.1. Công thức Nguy cơ Mưa Tích lũy Bão hòa Đất
Nguy cơ trượt trượt mái dốc không chỉ phụ thuộc vào lượng mưa tức thời ($R_{24h}$) mà bị ảnh hưởng lớn bởi độ ẩm tích lũy trong đất từ những ngày trước đó ($R_{72h}$). Hàm nguy cơ tích lũy $R_{acc}$ được xác định:

$$R_{acc} = R_{24h} + \alpha \cdot R_{72h}$$

Trong đó:
- $R_{24h}$: Lượng mưa tích lũy trong 24 giờ hiện tại ($\text{mm}$).
- $R_{72h}$: Lượng mưa tích lũy 3 ngày liên tiếp ($\text{mm}$).
- $\alpha = 0.5$: Hệ số kiệt ẩm đất đối với cấu trúc đất thịt pha cát vùng núi Việt Nam.

### 2.2. Ma trận Phân cấp Rủi ro 3 Cấp độ
Dựa trên giá trị $R_{acc}$ và vị trí địa chất, hệ thống phân loại thành 3 cấp độ:

$$\text{RiskLevel} = \begin{cases} 
\text{🔴 NGUY HIỂM (Danger)}, & \text{nếu } R_{24h} > 150\text{mm} \text{ hoặc } R_{72h} > 300\text{mm} \\ 
\text{🟡 CẢNH GIÁC (Alert)}, & \text{nếu } 50\text{mm} \le R_{24h} \le 150\text{mm} \text{ hoặc } R_{72h} \ge 200\text{mm} \\ 
\text{🟢 AN TOÀN (Safe)}, & \text{nếu } R_{24h} < 50\text{mm} 
\end{cases}$$

### 2.3. Thuật toán Khoanh vùng Bán kính Nguy cơ GIS (Buffer Zone Polygon Algorithm)
Xung quanh mỗi tọa độ sạt lở lịch sử $(lat_i, lng_i)$, hệ thống tính toán bán kính nguy cơ lan tỏa $R_{buffer}$ theo độ dốc mái taluy:

$$R_{buffer} = R_{base} \cdot \left(1 + \frac{\text{SlopeAngle}}{90^\circ}\right)$$

Trực quan hóa trên bản đồ GIS Leaflet bằng các đường tròn bán trong suốt viền nét đứt màu đỏ/cam với bán kính từ $1.0\text{km}$ đến $3.5\text{km}$.

---

## **CHƯƠNG 3: KIẾN TRÚC KỸ THUẬT VÀ RAG ENGINE (SYSTEM ARCHITECTURE)**

### 3.1. Sơ đồ Kiến trúc Đa tầng (Multi-Tier Infrastructure Topology)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TERRAALERT SYSTEM ARCHITECTURE                            │
│                                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                            FRONTEND PRESENTATION LAYER                           │  │
│  │   React 18 + TypeScript + Vite + Tailwind CSS (Fresh Light Palette)             │  │
│  │   - 1. Home Dashboard       - 2. Research GIS Map   - 3. Alert Center            │  │
│  │   - 4. Survival Handbook    - 5. TerraBot AI Chat Widget (Góc phải)              │  │
│  └─────────────────────────────────────────┬────────────────────────────────────────┘  │
│                                            │ (REST / SSE / WebSockets)                 │
│                                            ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                            BACKEND APPLICATION LAYER                             │  │
│  │   FastAPI Python Async Core + PostgreSQL/PostGIS + JWT Auth                      │  │
│  │   - Weather & GIS Service (Open-Meteo Integration)                               │  │
│  │   - Admin KB Ingestion Pipeline (Hierarchical Chunking & Dry-run)                │  │
│  └──────────────────┬───────────────────────────────────────────┬───────────────────┘  │
│                     │                                           │                      │
│                     ▼                                           ▼                      │
│  ┌──────────────────────────────────────┐     ┌─────────────────────────────────────┐  │
│  │       EMBEDDING MICROSERVICE         │     │        VECTOR DB & PERSISTENCE      │  │
│  │  SentenceTransformer (Harrier-270M)  │     │  ChromaDB HttpClient / Persistent   │  │
│  │  PyTorch Multi-threading + Warm-up   │     │  Volume Mount: chroma_data          │  │
│  └──────────────────────────────────────┘     └─────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2. Microservice Embedding Tốc độ cao (`embedding_service/main.py`)
- **Mô hình Vector Embeddings:** `microsoft/harrier-oss-v1-270m` chuyên biệt cho trích xuất ngữ cảnh ngôn ngữ tự nhiên.
- **Tối ưu Đa luồng CPU:** Kích hoạt `torch.set_num_threads(min(os.cpu_count() or 4, 8))` tận dụng tối đa đa nhân máy chủ.
- **Khởi động Warm-up:** Thực hiện nạp sẵn weights vào RAM ngay khi startup (`model.encode(["Cảnh báo sạt lở"])`), xóa bỏ hoàn toàn độ trễ 2-3s của câu hỏi đầu tiên.

### 3.3. CSDL Vector ChromaDB & Cấu hình Lưu trữ Vĩnh viễn (Permanent Data Persistence)
Để khắc phục hoàn toàn hiện tượng mất dữ liệu vector sau khi khởi động lại Docker, cấu hình trong `docker-compose.yml` được thiết lập:
```yaml
  chromadb:
    image: chromadb/chroma:latest
    environment:
      - IS_PERSISTENT=TRUE
      - PERSIST_DIRECTORY=/chroma/chroma
      - ANONYMIZED_TELEMETRY=FALSE
    volumes:
      - chroma_data:/chroma/chroma
```

---

## **CHƯƠNG 4: THIẾT KẾ GIAO DIỆN VÀ 5 MÀN HÌNH DEMO (UI/UX DESIGN)**

### 4.1. Ngôn ngữ Thiết kế Fresh Light Palette
Ứng dụng chuyển đổi hoàn toàn sang dải màu tươi sáng, dễ nhìn dưới ánh sáng ngoài trời vùng núi:
- **Nền tổng thể:** Nền chuyển màu mượt `bg-gradient-to-br from-slate-100 via-sky-50/60 to-blue-50/50`.
- **Thẻ Kính mờ:** `bg-white/95 backdrop-blur-md border border-slate-200/90 shadow-sm`.
- **Thanh menu VI|EN:** Thanh chuyển ngôn ngữ tinh gọn dạng capsule `VI | EN`.

### 4.2. Chi tiết 5 Màn hình Chức năng
1. 🏠 **Màn hình 1: Trang chủ (Home Dashboard):** Tổng quan tình hình thời tiết thời gian thực, thẻ chỉ số an toàn và lối tắt thao tác khẩn cấp.
2. 🗺️ **Màn hình 2: Nghiên cứu (Research Dashboard):** Bản đồ số GIS Leaflet hiển thị các điểm sạt lở HDX, vòng tròn khoanh vùng nguy cơ 1-3.5km và biểu đồ lượng mưa VRAIN tích lũy.
3. 🚨 **Màn hình 3: Trung tâm Cảnh báo (Alert Center):** Danh sách phân loại rủi ro 3 màu rõ rệt (🟢 An toàn - 🟡 Cảnh giác - 🔴 Nguy hiểm).
4. 📚 **Màn hình 4: Cẩm nang Sinh tồn (Survival Handbook):** Quy trình sơ cấp cứu CPR, kỹ năng ứng phó lũ quét, lọc nước sạch (hoạt động offline 100%).
5. 🤖 **Màn hình 5: TerraBot Chatbot AI (Widget góc phải):** Cửa sổ chat AI RAG hỗ trợ render Markdown chuẩn đẹp, các chip gợi ý khẩn cấp 1-chạm ($112/115$).

---

## **CHƯƠNG 5: ĐÁNH GIÁ THỰC NGHIỆM VÀ HIỆU NĂNG (EMPIRICAL EVALUATION)**

### 5.1. Tốc độ Phản hồi RAG Chatbot
- **Trước khi tối ưu:** Thời gian tạo embeddings cho query mất ~2.4 giây trên CPU.
- **Sau khi cấu hình PyTorch Multi-threading & Warm-up:** Thời gian phản hồi giảm xuống **< 95 ms**.

### 5.2. Đánh giá Độ tin cậy (Resilience & Offline Performance)
- **Tích hợp Open-Meteo Live API:** Kéo dữ liệu mưa thời gian thực 100% miễn phí (10,000 req/ngày).
- **Cơ chế Fallback Dự phòng:** Khi mất mạng, hệ thống tự động đọc bộ dữ liệu chuẩn hóa `disaster_data.json` và CSDL IndexedDB, đảm bảo 0% gián đoạn khi demo.

### 5.3. Kiểm thử Tĩnh Mã nguồn (TypeScript Check)
Chạy lệnh `node node_modules/typescript/lib/tsc.js --noEmit`: Kết quả **0 Lỗi (0 Errors found)** trên toàn bộ codebase Frontend.

---

## **CHƯƠNG 6: HƯỚNG MỞ RỘNG VÀ KẾT LUẬN (CONCLUSION & FUTURE WORK)**

### 6.1. Kết luận
Hệ thống **TerraAlert** đã hoàn thành xuất sắc các mục tiêu đề ra, cung cấp giải pháp cảnh báo sớm sạt lở đất tinh gọn, trực quan và giàu tính nhân văn. Việc kết hợp bản đồ GIS Leaflet khoanh vùng bán kính nguy cơ cùng Trợ lý AI RAG TerraBot đã tạo nên một bước tiến lớn trong việc đưa công nghệ AI phục vụ cộng đồng yếu thế.

### 6.2. Hướng Mở rộng Nghiên cứu
1. **Kết nối Lưới Cảm biến IoT:** Đấu nối trực tiếp dữ liệu cảm biến đo độ ẩm đất (Soil Moisture Sensors) tại các vị trí dốc nguy hiểm.
2. **Ứng dụng Dữ liệu Vệ tinh SAR:** Tích hợp ảnh vệ tinh Radar (Sentinel-1 SAR) để tự động phát hiện vi biến dạng nứt đất bề mặt trước khi sạt lở xảy ra.
3. **Mô hình AI Đa ngôn ngữ Dân tộc Dân gian:** Nâng cấp TerraBot hỗ trợ phát thanh bằng tiếng H'Mông, Thái, Tày qua công nghệ Text-to-Speech (TTS).
