# Hướng Dẫn Tạo Dataset & Huấn luyện Mô hình Landslide Susceptibility

## Tổng Quan

```
┌─────────────────────────────────────────────────────────────────┐
│  BƯỚC 1: TẠO DATASET                                           │
│  python create_dataset.py --mode api --output dataset.csv       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  BƯỚC 2: UPLOAD LÊN KAGGLE                                     │
│  Upload dataset.csv → New Notebook → Run All                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  BƯỚC 3: DOWNLOAD MODEL                                         │
│  Download output/ → Copy vào backend/app/slow_lane/ml/models/   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Bước 1: Tạo Dataset

### Cài đặt thư viện

```bash
pip install pandas numpy requests meteostat
```

### Các chế độ chạy

| Chế độ | Lệnh | Dữ liệu thật | Cần đăng ký |
|--------|------|---------------|-------------|
| Synthetic | `--mode synthetic` | Không | Không |
| API | `--mode api` | Có | Không |
| GEE | `--mode gee` | Có | Cần (1-7 ngày) |

### Chạy synthetic (Test nhanh)

```bash
cd ml_training/scripts
python create_dataset.py --mode synthetic --output dataset.csv
```

Output: 2000 mẫu, features random. Dùng để test pipeline.

### Chạy với API miễn phí (Khuyến nghị)

```bash
cd ml_training/scripts

# Không có file HDX (dùng sample data)
python create_dataset.py --mode api --output dataset.csv

# Có file HDX
python create_dataset.py --mode api --output dataset.csv --hdx path/to/hdx.csv

# Không dùng Meteostat (nhanh hơn)
python create_dataset.py --mode api --output dataset.csv --no-meteostat
```

**Features được tạo:**

| Feature | Nguồn | Mô tả |
|---------|-------|-------|
| `elevation` | Open Elevation API | Độ cao (m) |
| `slope` | Ước tính từ elevation | Độ dốc (độ) |
| `aspect` | Random | Hướng dốc (0-360) |
| `annual_precipitation` | Meteostat API | Lượng mưa năm (mm) |
| `max_daily_rainfall` | Meteostat API | Mưa max ngày (mm) |
| `rainfall_intensity` | Meteostat API | Cường độ mưa TB |
| `ndvi` | Ước tính | Chỉ số thực vật |
| `distance_to_fault` | Tính toán | Khoảng cách đứt gãy (km) |

### Chạy với Google Earth Engine

```bash
# Bước 1: Đăng ký GEE (https://earthengine.google.com/)
# Bước 2: Chờ duyệt (1-7 ngày)
# Bước 3: Authenticate
python -c "import ee; ee.Authenticate()"

# Bước 4: Chạy script
python create_dataset.py --mode gee --output dataset.csv --hdx path/to/hdx.csv
```

---

## Bước 2: Lấy Ground Truth (Lịch sử sạt lở)

### Nguồn 1: HDX - Humanitarian Data Exchange

**URL:** https://data.humdata.org/

1. Vào https://data.humdata.org/
2. Search: `Vietnam landslide` hoặc `Vietnam disaster`
3. Download CSV với cột `latitude`, `longitude`

### Nguồn 2: DesInventar Sendai (UNDRR)

**URL:** https://www.desinventar.net/

1. Chọn **Country: Vietnam**
2. Chọn **Disaster Type: Landslide**
3. Export → Download CSV

### Nguồn 3: Kaggle

Search: `global landslide`, `Vietnam disaster`

---

## Bước 3: Upload lên Kaggle và Train

### 3.1. Tạo Kaggle Notebook

1. Vào https://www.kaggle.com/code
2. Click **New Notebook**

### 3.2. Upload Dataset

1. Ở panel phải, tab **Files**
2. Click **Upload**
3. Chọn file `dataset.csv` đã tạo ở Bước 1

### 3.3. Upload Notebook

1. Download file `landslide_susceptibility_training.ipynb`
2. Trên Kaggle: **File** → **Import Notebook** → **Upload**

### 3.4. Chạy Notebook

1. Click **Run All** (hoặc Shift+Enter từng cell)
2. Đợi 5-10 phút
3. Kết quả sẽ hiển thị trực tiếp trên notebook

### 3.5. Download Model

1. Sau khi chạy xong, scroll xuống cuối notebook
2. Ở panel **Output** bên phải, download các file `.pkl` và `.json`
3. Hoặc vào tab **Files** → **output/** → download từng file

---

## Bước 4: Tích hợp vào Backend

### 4.1. Copy model files

```
backend/app/slow_lane/ml/models/
├── lsm_xgboost_model.pkl
├── lsm_random_forest_model.pkl
├── label_encoders.pkl
└── model_metadata.json
```

### 4.2. Restart Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 4.3. Test API

```bash
curl http://localhost:8000/api/v1/slow-lane/map/susceptibility?lat=16.05&lon=108.20
```

---

## Troubleshooting

### Lỗi: Open Elevation API timeout

```bash
# Thử lại sau hoặc dùng --no-meteostat để skip
python create_dataset.py --mode api --output dataset.csv --no-meteostat
```

### Lỗi: Meteostat không có dữ liệu

```bash
# Dùng --no-meteostat
python create_dataset.py --mode api --output dataset.csv --no-meteostat
```

### Lỗi: Rate limit API

```bash
# Script đã có sleep() giữa các request. Nếu vẫn lỗi, tăng thời gian chờ.
```

### Lỗi: Kaggle notebook không tìm thấy file

```bash
# Đảm bảo upload file CSV trước khi chạy notebook
# Path đúng: /kaggle/working/landslide_dataset.csv
```

---

## Tóm tắt nhanh

```bash
# 1. Tạo dataset (chọn 1 trong 3)
python ml_training/scripts/create_dataset.py --mode synthetic --output dataset.csv   # Test
python ml_training/scripts/create_dataset.py --mode api --output dataset.csv         # Thật

# 2. Upload dataset.csv lên Kaggle Files

# 3. Chạy notebook landslide_susceptibility_training.ipynb trên Kaggle

# 4. Download model files từ output/

# 5. Copy vào backend/app/slow_lane/ml/models/
```
