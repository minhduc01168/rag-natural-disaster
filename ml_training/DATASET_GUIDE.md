# Hướng Dẫn Tạo Dataset Landslide Susceptibility Từ Nguồn Công Cộng

## Tổng Quan Quy Trình

```
┌─────────────────────────────────────────────────────────────────┐
│                    NGUỒN DỮ LIỆU                                │
├─────────────────────────────────────────────────────────────────┤
│  1. HDX/DesInventar → Ground Truth (vị trí sạt lở lịch sử)     │
│  2. GEE + SRTM     → Địa hình (elevation, slope, aspect)       │
│  3. GEE + GPM      → Lượng mưa (precipitation)                 │
│  4. GEE + Sentinel2 → Thảm thực vật (NDVI)                     │
│  5. Meteostat API   → Dữ liệu khí tượng bổ sung               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    GHÉP DỮ LIỆU                                 │
│  Positive samples: Vị trí sạt lở + features tại vị trí đó      │
│  Negative samples: Random points + features tại vị trí đó       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT                                        │
│  landslide_dataset.csv (dùng để train ML trên Kaggle)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phần 1: Lấy Ground Truth (Lịch sử sạt lở)

### Nguồn 1: HDX - Humanitarian Data Exchange

**URL:** https://data.humdata.org/

**Cách lấy:**

1. Vào https://data.humdata.org/
2. Search: `Vietnam landslide` hoặc `Vietnam disaster`
3. Chọn dataset có format **GeoJSON** hoặc **CSV** với cột `latitude`, `longitude`
4. Download file

**Dataset推荐:**
- `disaster-locations-vietnam` - Vị trí thiên tai Việt Nam
- `vietnam-flood-landslide` - Lũ lụt & sạt lở

### Nguồn 2: DesInventar Sendai (UNDRR)

**URL:** https://www.desinventar.net/

**Cách lấy:**

1. Vào https://www.desinventar.net/
2. Chọn **Country: Vietnam**
3. Chọn **Disaster Type: Landslide**
4. Export data → Download CSV/Shapefile

### Nguồn 3: NASA GLC (Global Landslide Catalog)

**URL:** https://data.nasa.gov/ (search "landslide")

**Cách lấy:**

1. Vào https://data.nasa.gov/
2. Search: `global landslide catalog`
3. Download CSV (có cột `latitude`, `longitude`, `landslide_trigger`, `landslide_size`)

### Nguồn 4: Kaggle Datasets

Search trên Kaggle:
- `Vietnam disaster`
- `Southeast Asia landslide`
- `flood landslide Vietnam`

---

## Phần 2: Lấy dữ liệu từ Google Earth Engine (GEE)

### Bước 1: Đăng ký GEE

1. Vào https://earthengine.google.com/
2. Sign in với Google account
3. Click **"Register a Noncommercial or Research Cloud project"**
4. Điền thông tin → Chờ duyệt (1-2 ngày)

### Bước 2: Cài đặt Earth Engine Python API

```bash
pip install earthengine-api
```

### Bước 3: Authenticate

```python
import ee
ee.Authenticate()  # Mở browser, copy authorization code
ee.Initialize()
```

### Bước 4: Trích xuất dữ liệu từ GEE

Xem file script bên dưới 👇

---

## Phần 3: Script Python tổng hợp

Xem file: `scripts/create_dataset.py`

---

## Phần 4: Chạy trên Kaggle

1. Upload `landslide_dataset.csv` lên Kaggle Files
2. Chạy notebook `landslide_susceptibility_training.ipynb`
3. Download model files
