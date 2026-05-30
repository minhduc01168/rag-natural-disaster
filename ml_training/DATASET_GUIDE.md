# Hướng Dẫn Tạo Dataset Landslide Susceptibility

## Tổng Quan Quy Trình

```
┌─────────────────────────────────────────────────────────────────┐
│                    NGUỒN DỮ LIỆU                                │
├─────────────────────────────────────────────────────────────────┤
│  1. HDX/DesInventar → Ground Truth (vị trí sạt lở lịch sử)     │
│  2. SRTM DEM        → Địa hình (elevation, slope, aspect)      │
│  3. CHIRPS/GPM      → Lượng mưa (precipitation)                │
│  4. Sentinel-2      → Thảm thực vật (NDVI)                     │
│  5. OpenStreetMap   → Đường, sông, ranh giới                   │
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

Đây là bước **quan trọng nhất** - xác định vị trí đã xảy ra sạt lở.

### Nguồn 1: HDX - Humanitarian Data Exchange (Khuyến nghị)

**URL:** https://data.humdata.org/

**Cách lấy:**

1. Vào https://data.humdata.org/
2. Search: `Vietnam landslide` hoặc `Vietnam disaster`
3. Chọn dataset có format **CSV** hoặc **GeoJSON**
4. Click **Download** → Chọn file CSV

**Dataset đề xuất:**
- `disaster-locations-vietnam` - Vị trí thiên tai Việt Nam
- `vietnam-flood-landslide` - Lũ lụt & sạt lở
- `global-landslide-catalog` - Catalog sạt lở toàn cầu

**Format CSV mong đợi:**
```csv
latitude,longitude,event_date,disaster_type
16.05,108.20,2020-10-15,landslide
15.60,108.35,2020-10-18,landslide
```

### Nguồn 2: DesInventar Sendai (UNDRR)

**URL:** https://www.desinventar.net/

**Cách lấy:**

1. Vào https://www.desinventar.net/
2. Chọn **Country: Vietnam**
3. Chọn **Disaster Type: Landslide**
4. Click **Export** → Download CSV/Shapefile

### Nguồn 3: NASA Global Landslide Catalog

**URL:** https://data.nasa.gov/

**Cách lấy:**

1. Vào https://data.nasa.gov/
2. Search: `global landslide catalog`
3. Click vào dataset → **Export** → **CSV**

### Nguồn 4: Dữ liệu Việt Nam (VNDMS)

**URL:** https://vndms.dmc.gov.vn/

**Cách lấy:**

1. Vào trang web VNDMS
2. Tìm mục "Dữ liệu thiên tai" hoặc "Bản đồ thiên tai"
3. Download dữ liệu sạt lở (nếu có)

### Nguồn 5: Kaggle Datasets

**URL:** https://www.kaggle.com/datasets

**Cách lấy:**

1. Search: `landslide`, `natural disaster Vietnam`, `flood landslide`
2. Download dataset phù hợp

---

## Phần 2: Lấy dữ liệu đặc trưng (Features)

Có **3 phương pháp** từ dễ đến khó:

---

### Phương pháp A: Không cần GEE (Khuyến nghị cho người mới)

Dùng các API miễn phí và dữ liệu có sẵn.

#### 2A.1 - Dữ liệu địa hình (Elevation, Slope)

**Nguồn:** Open Elevation API (miễn phí, không cần đăng ký)

```python
import requests

def get_elevation_open(lat, lon):
    """Lấy độ cao từ Open Elevation API."""
    url = "https://api.open-elevation.com/api/v1/lookup"
    params = {"locations": f"{lat},{lon}"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['results'][0]['elevation']
    return None

# Ví dụ
elevation = get_elevation_open(16.05, 108.20)
print(f"Elevation: {elevation}m")
```

**Lưu ý:** API này có rate limit (~1 request/giây). Nếu cần nhiều điểm, batch processing.

**Nguồn bổ sung:** SRTM data download trực tiếp
- URL: https://earthexplorer.usgs.gov/
- Chọn dataset: **SRTM 1 Arc-Second Global**
- Download tile cho khu vực Việt Nam

#### 2A.2 - Dữ liệu lượng mưa (Precipitation)

**Nguồn 1: Meteostat API (miễn phí)**

```python
# Cài đặt: pip install meteostat
from meteostat import Point, Daily
from datetime import datetime

def get_precipitation(lat, lon, year=2022):
    """Lấy dữ liệu mưa từ Meteostat."""
    location = Point(lat, lon)
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    
    data = Daily(location, start, end)
    data = data.fetch()
    
    if not data.empty:
        return {
            'annual_precipitation': data['prcp'].sum(),  # mm/năm
            'max_daily_rainfall': data['prcp'].max(),    # mm/ngày
            'rainfall_intensity': data['prcp'].mean(),   # mm/ngày TB
        }
    return None

# Ví dụ
precip = get_precipitation(16.05, 108.20, 2022)
print(precip)
```

**Nguồn 2: OpenWeatherMap (Free Tier)**

- Đăng ký: https://openweathermap.org/api
- Free tier: 1000 calls/ngày
- API: `/onecall/timemachine` cho dữ liệu lịch sử

#### 2A.3 - Dữ liệu NDVI (Thảm thực vật)

**Nguồn: Sentinel Hub (miễn phí cho nghiên cứu)**

```python
# Đăng ký: https://www.sentinel-hub.com/
# Free tier: 30,000 processing units/tháng

import requests

def get_ndvi_sentinel(lat, lon, api_key):
    """Lấy NDVI từ Sentinel Hub."""
    url = "https://services.sentinel-hub.com/api/v1/process"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Request NDVI cho 1 điểm
    payload = {
        "input": {
            "bounds": {
                "bbox": [lon-0.01, lat-0.01, lon+0.01, lat+0.01]
            },
            "data": [{"type": "sentinel-2-l2a"}]
        },
        "evalscript": """
        //NDVI
        let val = (B08 - B04) / (B08 + B04);
        return [val];
        """
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```

**Nguồn thay thế: MODIS NDVI (NASA)**

- URL: https://lpdaac.usgs.gov/products/mod13q1v061/
- Download trực tiếp, không cần GEE

#### 2A.4 - Khoảng cách đến đứt gãy (Fault Lines)

**Nguồn: USGS Fault Database**

- URL: https://www.usgs.gov/programs/earthquake-hazards/faults
- Download shapefile → Tính khoảng cách bằng Python

```python
import geopandas as gpd
from shapely.geometry import Point

def calc_fault_distance(lat, lon, fault_shapefile):
    """Tính khoảng cách đến đứt gãy gần nhất."""
    faults = gpd.read_file(fault_shapefile)
    point = Point(lon, lat)
    
    # Tính khoảng cách đến tất cả đứt gãy (đơn vị: độ → km)
    distances = faults.geometry.distance(point) * 111  # 1 độ ≈ 111km
    return distances.min()
```

---

### Phương pháp B: Dùng Google Colab + GEE (Không cần chờ duyệt)

**Bước 1:** Vào https://colab.research.google.com/

**Bước 2:** Tạo notebook mới

**Bước 3:** Chạy cell sau:

```python
# Cài đặt Earth Engine
!pip install earthengine-api

# Authenticate (sẽ mở popup)
import ee
ee.Authenticate()

# Initialize
ee.Initialize(project='your-project-id')  # Hoặc bỏ qua nếu đã auth

# Test
print(ee.Image('USGS/SRTMGL1_003').getInfo())
```

**Lưu ý:** Cần có Google Cloud Project. Tạo tại https://console.cloud.google.com/

---

### Phương pháp C: Dùng Google Earth Engine (Chờ duyệt)

**Bước 1:** Đăng ký GEE
1. Vào https://earthengine.google.com/
2. Sign in với Google account
3. Click **"Register a Noncommercial or Research Cloud project"**
4. Điền thông tin:
   - Project name: `terraalert-lsm`
   - Purpose: `Research - Landslide Susceptibility Mapping`
   - Country: `Vietnam`
5. Submit → Chờ duyệt (1-7 ngày)

**Bước 2:** Sau khi được duyệt

```bash
pip install earthengine-api
python -c "import ee; ee.Authenticate()"
```

**Bước 3:** Chạy script

```bash
python ml_training/scripts/create_dataset.py --output dataset.csv
```

---

## Phần 3: Script Python tổng hợp

### Cách 1: Chạy synthetic (Test nhanh)

```bash
python ml_training/scripts/create_dataset.py --output dataset.csv --no-gee
```

**Output:** 2000 mẫu, features random. Dùng để test pipeline.

### Cách 2: Chạy với dữ liệu thật (Không cần GEE)

```python
# create_dataset_manual.py
import pandas as pd
import numpy as np
import requests
from meteostat import Point, Daily
from datetime import datetime

# 1. Load ground truth từ HDX
hdx_df = pd.read_csv('path/to/hdx_data.csv')  # Download từ HDX

# 2. Lấy features cho mỗi điểm
records = []
for _, row in hdx_df.iterrows():
    lat, lon = row['latitude'], row['longitude']
    
    # Lấy elevation
    elev_resp = requests.get(f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}")
    elevation = elev_resp.json()['results'][0]['elevation'] if elev_resp.ok else 0
    
    # Lấy precipitation
    location = Point(lat, lon)
    weather = Daily(location, datetime(2022,1,1), datetime(2022,12,31)).fetch()
    precip = weather['prcp'].sum() if not weather.empty else 1500
    
    records.append({
        'latitude': lat,
        'longitude': lon,
        'elevation': elevation,
        'slope': np.random.exponential(15),  # Placeholder
        'annual_precipitation': precip,
        'ndvi': np.random.uniform(0.2, 0.6),  # Placeholder
        'landslide': 1
    })

# 3. Tạo negative samples
# ... (tương tự với label = 0)

# 4. Save
df = pd.DataFrame(records)
df.to_csv('dataset.csv', index=False)
```

### Cách 3: Chạy với GEE

```bash
python ml_training/scripts/create_dataset.py --output dataset.csv --hdx path/to/hdx.csv
```

---

## Phần 4: Upload lên Kaggle và Train

1. Vào https://www.kaggle.com/code → **New Notebook**
2. Tab **Files** → **Upload** → Chọn `dataset.csv`
3. Chạy notebook `landslide_susceptibility_training.ipynb`
4. Download model files từ output

---

## Bảng so sánh các phương pháp

| Phương pháp | Thời gian | Dữ liệu thật | Độ khó |
|-------------|-----------|---------------|--------|
| A: API miễn phí | 1-2 giờ | Có | Dễ |
| B: Colab + GEE | 30 phút | Có | Trung bình |
| C: GEE chính thức | 1-7 ngày (chờ duyệt) | Có | Trung bình |
| Synthetic (`--no-gee`) | 1 phút | Không | Rất dễ |

---

## Khuyến nghị

1. **Bắt đầu với synthetic** (`--no-gee`) để test toàn bộ pipeline
2. **Sau đó dùng Phương pháp A** (API miễn phí) để tạo dataset thật
3. **Đăng ký GEE** song song, dùng sau khi được duyệt

---

## Troubleshooting

### Lỗi: Open Elevation API timeout
```python
# Thử endpoint khác
url = "https://api.open-elevation.com/api/v1/lookup"
# Hoặc dùng Elevation API khác
# https://open-meteo.com/en/docs/elevation-api
```

### Lỗi: Meteostat không có dữ liệu
```python
# Thử tọa độ gần nhất có dữ liệu
# Hoặc dùng OpenWeatherMap thay thế
```

### Lỗi: Rate limit API
```python
import time
time.sleep(1)  # Chờ 1 giây giữa các request
```
