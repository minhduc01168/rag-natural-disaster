# TÀI LIỆU CHUẨN KỸ THUẬT & KIẾN TRÚC DỮ LIỆU GIS
## HỆ THỐNG CẢNH BÁO SỚM THIÊN TAI VÀ NGUY CƠ SẠT LỞ ĐẤT TERRAALERT

---

## 1. ĐẶT VẤN ĐỀ VÀ MỤC TIÊU NGHIÊN CỨU

Hệ thống **TerraAlert** tập trung giải quyết bài toán cảnh báo sớm sạt lở đất và lũ quét cho khu vực miền núi phía Bắc Việt Nam thông qua việc:
1. Phân tích mối liên hệ giữa **Cường độ mưa tích lũy thời gian thực (Rainfall Intensity & Cumulative Precipitation)** và **Độ ẩm bão hòa đất tại các điểm nóng địa chất lịch sử**.
2. Xây dựng **Bản đồ Tương tác GIS Leaflet** với tính năng khoanh vùng bán kính nguy cơ trượt lở lan tỏa ($1.0\text{km} - 3.5\text{km}$).
3. Cung cấp **Trợ lý AI RAG (TerraBot)** giúp người dân và cán bộ địa phương tra cứu kỹ năng sinh tồn, kịch bản ứng phó khẩn cấp và danh bạ cứu hộ $112/115$.

---

## 2. NGUỒN DỮ LIỆU VÀ TÍNH PHÁP LÝ (DATA GOVERNANCE)

| Thành phần Dữ liệu | Nguồn Cung cấp | Chuẩn Kết nối API / Định dạng | Tính Pháp lý & Độ Tin cậy |
| :--- | :--- | :--- | :--- |
| **Lượng mưa Thời gian thực & Tích lũy (Realtime Rainfall)** | **Open-Meteo Weather API** (`open-meteo.com`) | RESTful JSON API<br>*(Free 100%, 10,000 req/ngày, No API Key)* | **Chính thức**: Nguồn dữ liệu khí tượng toàn cầu từ các mô hình dự báo ECMWF/GSMaP. |
| **Điểm nóng Sạt lở & Lũ quét Lịch sử** | **HDX** (UN OCHA) & Bộ Tài nguyên & Môi trường | CKAN REST API / GeoJSON | **Chính thức**: Dữ liệu công bố bởi Liên Hợp Quốc và Viện Khoa học Địa chất (Bộ TN&MT). |
| **Sổ tay Kỹ năng Sinh tồn & Sơ cứu** | Cục PCTT (Bộ NN&PTNT) & UNICEF | Vector Embeddings / ChromaDB | **Chính thức**: Tài liệu truyền thông và văn bản hướng dẫn chuẩn hóa của Chính phủ. |
| **Dữ liệu Quan trắc Dự phòng (Fallback)** | Trạm quan trắc tự động **VRAIN** (`vrain.vn`) | Local Standardized GeoJSON | **Dự phòng**: Đảm bảo hệ thống hoạt động 100% khi mất mạng hoặc nghẽn API ngoài. |

---

## 3. THÔNG SỐ TÍCH HỢP OPEN-METEO WEATHER API

Open-Meteo cung cấp API truy xuất lượng mưa theo tọa độ vĩ độ (`latitude`) và kinh độ (`longitude`) hoàn toàn miễn phí.

### Endpoint kỹ thuật:
```http
GET https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LNG}&current=precipitation,rain&daily=precipitation_sum&timezone=Asia%2FBangkok
```

### Cấu trúc Response đại diện (Tọa độ Sa Pa, Lào Cai: `22.3364, 103.8438`):
```json
{
  "latitude": 22.3198,
  "longitude": 103.8676,
  "timezone": "Asia/Bangkok",
  "elevation": 1514.0,
  "current_units": {
    "precipitation": "mm",
    "rain": "mm"
  },
  "current": {
    "time": "2026-08-08T16:00",
    "precipitation": 12.5,
    "rain": 12.5
  },
  "daily_units": {
    "precipitation_sum": "mm"
  },
  "daily": {
    "time": ["2026-08-08", "2026-08-09", "2026-08-10"],
    "precipitation_sum": [185.0, 142.0, 68.5]
  }
}
```

---

## 4. MÔ HÌNH NGUYỄNG MƯA & PHÂN CẤP CẢNH BÁO 3 CẤP ĐỘ

Nguy cơ sạt trượt đất dốc phụ thuộc vào lượng mưa 24h và lượng mưa tích lũy 72h ($R_{acc} = R_{24h} + 0.5 \cdot R_{72h}$):

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                                 MA TRẬN PHÂN CẤP RỦI RO                                │
│                                                                                       │
│  🟢 CẤP 1 - AN TOÀN (GREEN)     🟡 CẤP 2 - CẢNH GIÁC (YELLOW)    🔴 CẤP 3 - NGUY HIỂM (RED)  │
│  - Mưa 24h < 50mm                - Mưa 24h từ 50 - 150mm         - Mưa 24h > 150mm         │
│  - Đất chưa bão hòa nước         - Tích lũy 72h > 200mm          - Tích lũy 72h > 300mm    │
│  - Rủi ro thấp                   - Nguy cơ trượt taluy dốc        - Kích hoạt sơ tán ngay   │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. CHUẨN TRỰC QUAN HÓA BẢN ĐỒ GIS LEAFLET

Bản đồ tại trang **Research Dashboard** ([ResearchPage.tsx](file:///home/mypc/rag-natural-disaster/frontend/src/pages/ResearchPage.tsx)) kết hợp đồng thời 2 thành phần GIS:

1. **Point Markers (Tâm điểm Vị trí)**:
   - Icon trạm khí tượng 🌧️: Hiển thị tên trạm, lượng mưa 24h và 72h.
   - Icon sạt lở 🔴/🟡: Hiển thị tọa độ vụ sạt lở lịch sử, quy mô và thông số địa chất.
2. **Buffer Risk Zone Polygons (Khoanh vùng Bán kính Nguy cơ)**:
   - Các vòng tròn bán kính $1.0\text{km} - 3.5\text{km}$ nét đứt màu đỏ/cam bán trong suốt xung quanh tâm sạt lở.
   - Thể hiện diện tích đất dốc bị ảnh hưởng bởi độ ẩm bão hòa nước và rủi ro trượt trượt lan tỏa.

---

## 6. KIẾN TRÚC CẬP NHẬT REAL-TIME & PHƯƠNG ÁN CHỐNG ĐỨT GÃY (RESILIENCE)

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                          LUỒNG CẬP NHẬT REALTIME & FALLBACK                           │
│                                                                                       │
│   [ Open-Meteo Free API ] ──(Kéo dữ liệu 5 phút/lần)──► [ FastAPI Backend Core ]       │
│                                                                 │                     │
│   [ HDX UN OCHA GIS ] ──────(GeoJSON Sạt lở lịch sử)────────────┤                     │
│                                                                 ▼                     │
│   [ Local Fallback Dataset ] ◄──(Tự động chuyển nếu lỗi API)─── Push Live Event (SSE) │
│                                                                 │                     │
│                                                                 ▼                     │
│                                                   [ Frontend React GIS Map ]          │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Tầng Backend Polling Engine:** FastAPI Async Worker tự động gửi request tới Open-Meteo định kỳ 5 phút/lần.
2. **Tầng Push Live Event:** Khi chỉ số mưa vượt ngưỡng, Backend gửi tín hiệu WebSocket/SSE xuống toàn bộ client.
3. **Tầng Frontend Realtime:** Trang `Research Dashboard` cập nhật Marker & Vòng tròn khoanh vùng mà không cần F5.
4. **Phương án Fallback:** Nếu mạng bị ngắt kết nối, hệ thống tự động chuyển sang CSDL `disaster_data.json` chuẩn hóa local, đảm bảo buổi thuyết trình demo luôn chạy mượt mà 100%.
