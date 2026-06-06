"""
Script tạo dataset Landslide Susceptibility cho ML Training

Các chế độ chạy:
1. --mode synthetic   : Tạo dữ liệu giả lập (test nhanh, không cần API)
2. --mode api         : Dùng API miễn phí (Open Elevation, Meteostat) - KHUYẾN NGHỊ
3. --mode gee         : Dùng Google Earth Engine (cần đăng ký trước)

Cách sử dụng:
    # Test nhanh với synthetic data
    python create_dataset.py --mode synthetic --output dataset.csv

    # Tạo dataset thật với API miễn phí (không cần đăng ký)
    python create_dataset.py --mode api --output dataset.csv --hdx path/to/hdx.csv

    # Dùng Google Earth Engine (cần đăng ký trước)
    python create_dataset.py --mode gee --output dataset.csv --hdx path/to/hdx.csv

Yêu cầu:
    pip install pandas numpy requests meteostat
"""

import pandas as pd
import numpy as np
import argparse
import os
import time
import requests
from datetime import datetime


# ============================================================
# HÀM TIỆN ÍCH
# ============================================================

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_step(step, total, text):
    print(f"\n[{step}/{total}] {text}")


# ============================================================
# 1. LOAD GROUND TRUTH (VỊ TRÍ SẠT LỞ)
# ============================================================

def load_ground_truth(hdx_csv_path=None):
    """
    Load vị trí sạt lở từ file CSV.
    
    Nếu không có file, dùng sample data tại Việt Nam.
    """
    if hdx_csv_path and os.path.exists(hdx_csv_path):
        df = pd.read_csv(hdx_csv_path)
        print(f"  Loaded {len(df)} records from {hdx_csv_path}")
        
        # Đảm bảo có cột latitude, longitude
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            # Thử tìm cột khác
            lat_cols = [c for c in df.columns if 'lat' in c.lower() or c.lower() in ['y', 'vĩ độ', 'vi do']]
            lon_cols = [c for c in df.columns if 'lon' in c.lower() or 'lng' in c.lower() or c.lower() in ['x', 'kinh độ', 'kinh do']]
            
            if lat_cols and lon_cols:
                df = df.rename(columns={lat_cols[0]: 'latitude', lon_cols[0]: 'longitude'})
            else:
                print("  WARNING: Cannot find lat/lon columns. Using sample data.")
                return get_sample_landslide_data()
        
        # Lọc dữ liệu hợp lệ
        df = df.dropna(subset=['latitude', 'longitude'])
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # TỰ ĐỘNG LỌC DỮ LIỆU THUỘC LÃNH THỔ VIỆT NAM (Dành cho Global Dataset)
        # Bounding box Việt Nam: Vĩ độ (8.0 -> 24.0), Kinh độ (102.0 -> 110.0)
        original_len = len(df)
        df = df[
            (df['latitude'].between(8.0, 24.0)) & 
            (df['longitude'].between(102.0, 110.0))
        ]
        
        print(f"  Filtered {len(df)} Vietnam records from {original_len} total global records.")
        
        if len(df) == 0:
            print("  WARNING: No records found in Vietnam bounds. Falling back to sample data.")
            return get_sample_landslide_data()
            
        return df
    else:
        print("  No HDX file provided. Using sample Vietnam landslide data.")
        return get_sample_landslide_data()


def get_sample_landslide_data(n_samples=500):
    """
    Sinh dữ liệu mô phỏng sạt lở (synthetic data) tại Việt Nam với số lượng lớn.
    Tập trung vào 3 vùng có nguy cơ cao: Tây Bắc, Miền Trung, Tây Nguyên.
    """
    # 3 vùng có nguy cơ sạt lở cao (Tây Bắc, Miền Trung, Tây Nguyên)
    regions = [
        {'lat_min': 21.0, 'lat_max': 23.0, 'lon_min': 103.0, 'lon_max': 105.5}, # Tây Bắc
        {'lat_min': 14.5, 'lat_max': 16.5, 'lon_min': 107.5, 'lon_max': 108.5}, # Miền Trung
        {'lat_min': 11.5, 'lat_max': 14.0, 'lon_min': 107.5, 'lon_max': 108.5}, # Tây Nguyên
    ]
    
    lats, lons = [], []
    for _ in range(n_samples):
        reg = regions[np.random.randint(0, len(regions))]
        lats.append(np.random.uniform(reg['lat_min'], reg['lat_max']))
        lons.append(np.random.uniform(reg['lon_min'], reg['lon_max']))
        
    df = pd.DataFrame({
        'latitude': lats,
        'longitude': lons,
        'landslide': 1,
        'event_date': '2023-08-10'  # Dummy date
    })
    
    print(f"  Generated {n_samples} synthetic landslide locations in Vietnam's mountainous regions.")
    return df


# ============================================================
# 2. TẠO NEGATIVE SAMPLES
# ============================================================

def generate_negative_samples(positive_df, ratio=1.0):
    """
    Tạo negative samples (điểm không có sạt lở) trong cùng khu vực.
    
    Args:
        positive_df: DataFrame chứa vị trí sạt lở
        ratio: Tỷ lệ negative/positive (mặc định 1:1)
    """
    n_negative = int(len(positive_df) * ratio)
    
    lat_min, lat_max = positive_df['latitude'].min() - 1, positive_df['latitude'].max() + 1
    lon_min, lon_max = positive_df['longitude'].min() - 1, positive_df['longitude'].max() + 1
    
    negative_df = pd.DataFrame({
        'latitude': np.random.uniform(lat_min, lat_max, n_negative),
        'longitude': np.random.uniform(lon_min, lon_max, n_negative),
        'landslide': 0
    })
    
    print(f"  Generated {n_negative} negative samples (ratio {ratio}:1)")
    return negative_df


# ============================================================
# 3. LẤY FEATURES TỪ API MIỄN PHÍ
# ============================================================

def get_elevation_from_api(lat, lon):
    """
    Lấy độ cao từ OpenTopoData API (Aster30m).
    Nguồn tin cậy hơn cho dữ liệu DEM 30m.
    URL: https://api.opentopodata.org/
    """
    for _ in range(3):  # Thử lại tối đa 3 lần với exponential backoff
        try:
            url = "https://api.opentopodata.org/v1/aster30m"
            params = {"locations": f"{lat},{lon}"}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result['results'] and result['results'][0]['elevation'] is not None:
                    return result['results'][0]['elevation']
            time.sleep(1)
        except Exception:
            time.sleep(2)
            pass
    
    return None


def get_elevation_batch(locations, batch_size=50):
    """
    Lấy độ cao theo batch (nhanh hơn gọi từng điểm).
    
    Args:
        locations: List of (lat, lon) tuples
        batch_size: Số điểm mỗi batch
    """
    elevations = []
    total = len(locations)
    
    for i in range(0, total, batch_size):
        batch = locations[i:i+batch_size]
        
        # Tạo query string cho batch
        loc_strings = [f"{lat},{lon}" for lat, lon in batch]
        locations_str = "|".join(loc_strings)
        
        try:
            url = "https://api.opentopodata.org/v1/aster30m"
            params = {"locations": locations_str}
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                results = response.json()['results']
                for r in results:
                    elevations.append(r['elevation'])
            else:
                elevations.extend([None] * len(batch))
        except Exception:
            elevations.extend([None] * len(batch))
        
        # Progress
        progress = min(i + batch_size, total)
        print(f"    Elevation: {progress}/{total} points", end='\r')
        
        time.sleep(1)  # Rate limit OpenTopoData (1 request/sec)
    
    print(f"    Elevation: {total}/{total} points - Done!")
    return elevations


def get_precipitation_from_meteostat(lat, lon, year=2022):
    """
    Lấy dữ liệu mưa từ Meteostat API.
    Docs: https://dev.meteostat.net/python/
    """
    try:
        from meteostat import Point, Daily
        
        location = Point(lat, lon)
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
        
        data = Daily(location, start, end)
        data = data.fetch()
        
        if not data.empty and data['prcp'].notna().sum() > 0:
            return {
                'annual_precipitation': float(data['prcp'].sum()),
                'max_daily_rainfall': float(data['prcp'].max()),
                'rainfall_intensity': float(data['prcp'].mean()),
            }
    except ImportError:
        pass
    except Exception:
        pass
    
    return None


def estimate_slope(elevation, lat, lon, nearby_elevations=None):
    """
    Ước tính độ dốc từ độ cao.
    Nếu có độ cao lân cận, tính chính xác hơn.
    """
    if nearby_elevations and len(nearby_elevations) >= 2:
        # Tính gradient từ các điểm lân cận
        diffs = [abs(elevation - e) for e in nearby_elevations if e is not None]
        if diffs:
            avg_diff = np.mean(diffs)
            # Giả sử khoảng cách ~1km giữa các điểm
            slope_deg = np.degrees(np.arctan(avg_diff / 1000))
            return max(0, min(90, slope_deg))
    
    # Fallback: ước tính dựa trên độ cao
    # Khu vực núi cao thường có độ dốc lớn hơn
    base_slope = np.random.exponential(12)
    elevation_factor = elevation / 500  # Độ cao càng cao → độ dốc trung bình越大
    return base_slope * (1 + elevation_factor * 0.3)


def estimate_ndvi(lat, lon, land_use=None):
    """
    Ước tính NDVI dựa trên vị trí địa lý và loại đất.
    
    NDVI trung bình tại Việt Nam:
    - Rừng: 0.6 - 0.8
    - Nông nghiệp: 0.3 - 0.6
    - Đô thị: 0.1 - 0.2
    - Trơ trọi: -0.1 - 0.1
    """
    # Ước tính dựa trên vĩ độ (miền Bắc có rừng nhiều hơn)
    if lat > 20:  # Miền Bắc núi cao
        base_ndvi = np.random.uniform(0.4, 0.7)
    elif lat > 16:  # Miền Trung
        base_ndvi = np.random.uniform(0.3, 0.6)
    else:  # Miền Nam
        base_ndvi = np.random.uniform(0.4, 0.7)
    
    return base_ndvi


def estimate_fault_distance(lat, lon):
    """
    Ước tính khoảng cách đến đứt gãy gần nhất.
    
    Các đứt gãy chính tại Việt Nam:
    - Đứt gãy sông Hồng (Hà Nội - Lào Cai)
    - Đứt gãy Đà Nẵng
    - Đứt gãy Kontum
    - Đứt gãy Đông Triều
    """
    # Tọa độ các đứt gãy chính
    fault_locations = [
        (21.0, 105.8),   # Sông Hồng
        (16.0, 108.2),   # Đà Nẵng
        (14.5, 108.0),   # Kontum
        (21.2, 106.8),   # Đông Triều
        (15.5, 107.5),   # Quảng Nam
        (18.0, 106.5),   # Nghệ An
        (12.0, 108.5),   # Nha Trang
        (10.8, 106.7),   # TP.HCM
    ]
    
    # Tính khoảng cách đến đứt gãy gần nhất
    min_dist = float('inf')
    for fault_lat, fault_lon in fault_locations:
        # Công thức Haversine (đơn giản hóa)
        dlat = np.radians(lat - fault_lat)
        dlon = np.radians(lon - fault_lon)
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat)) * np.cos(np.radians(fault_lat)) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        dist = 6371 * c  # km
        min_dist = min(min_dist, dist)
    
    return min_dist


# ============================================================
# 4. TẠO DATASET VỚI API MIỄN PHÍ
# ============================================================

def create_dataset_with_api(output_csv='landslide_dataset.csv', hdx_csv=None, use_meteostat=True):
    """
    Tạo dataset bằng API miễn phí (không cần GEE).
    
    Features:
    - elevation: Độ cao (m) - từ Open Elevation API
    - slope: Độ dốc (độ) - ước tính từ elevation
    - aspect: Hướng dốc (0-360) - random
    - annual_precipitation: Lượng mưa năm (mm) - từ Meteostat
    - max_daily_rainfall: Mưa max ngày (mm) - từ Meteostat
    - rainfall_intensity: Cường độ mưa TB (mm/day) - từ Meteostat
    - ndvi: Chỉ số thực vật - ước tính
    - distance_to_fault: Khoảng cách đứt gãy (km) - tính toán
    """
    print_header("TẠO DATASET VỚI API MIỄN PHÍ")
    
    # 1. Load ground truth
    print_step(1, 5, "Loading ground truth (landslide locations)...")
    positive_df = load_ground_truth(hdx_csv)
    positive_df['landslide'] = 1
    print(f"  Positive samples: {len(positive_df)}")
    
    # 2. Generate negative samples
    print_step(2, 5, "Generating negative samples...")
    negative_df = generate_negative_samples(positive_df, ratio=1.0)
    
    # 3. Merge và lấy features
    print_step(3, 5, "Extracting elevation from Open Elevation API...")
    all_df = pd.concat([positive_df, negative_df], ignore_index=True)
    all_df = all_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    locations = list(zip(all_df['latitude'], all_df['longitude']))
    elevations = get_elevation_batch(locations, batch_size=50)
    all_df['elevation'] = elevations
    
    # Fill missing elevation với giá trị trung bình
    median_elev = all_df['elevation'].median()
    all_df['elevation'] = all_df['elevation'].fillna(median_elev)
    
    # 4. Tính các features khác
    print_step(4, 5, "Computing other features...")
    
    # Slope (ước tính)
    all_df['slope'] = all_df.apply(
        lambda row: estimate_slope(row['elevation'], row['latitude'], row['longitude']),
        axis=1
    )
    
    # Aspect (hướng dốc - random vì cần DEM thật)
    all_df['aspect'] = np.random.uniform(0, 360, len(all_df))
    
    # Distance to fault
    all_df['distance_to_fault'] = all_df.apply(
        lambda row: estimate_fault_distance(row['latitude'], row['longitude']),
        axis=1
    )
    
    # NDVI (ước tính)
    all_df['ndvi'] = all_df.apply(
        lambda row: estimate_ndvi(row['latitude'], row['longitude']),
        axis=1
    )
    
    # Precipitation (từ Meteostat nếu có)
    if use_meteostat:
        print("  Fetching precipitation from Meteostat...")
        precip_data = []
        for idx, row in all_df.iterrows():
            precip = get_precipitation_from_meteostat(row['latitude'], row['longitude'])
            if precip:
                precip_data.append(precip)
            else:
                # Default values cho Việt Nam
                precip_data.append({
                    'annual_precipitation': np.random.normal(1800, 400),
                    'max_daily_rainfall': np.random.normal(80, 25),
                    'rainfall_intensity': np.random.normal(5, 2),
                })
            
            if (idx + 1) % 10 == 0:
                print(f"    Precipitation: {idx+1}/{len(all_df)} points", end='\r')
            time.sleep(0.2)  # Rate limit
        
        print(f"    Precipitation: {len(all_df)}/{len(all_df)} points - Done!")
        
        precip_df = pd.DataFrame(precip_data)
        all_df = pd.concat([all_df, precip_df], axis=1)
    else:
        # Default values
        all_df['annual_precipitation'] = np.random.normal(1800, 400, len(all_df))
        all_df['max_daily_rainfall'] = np.random.normal(80, 25, len(all_df))
        all_df['rainfall_intensity'] = np.random.normal(5, 2, len(all_df))
    
    # Ensure positive values
    all_df['elevation'] = all_df['elevation'].abs()
    all_df['slope'] = all_df['slope'].abs()
    all_df['annual_precipitation'] = all_df['annual_precipitation'].abs()
    all_df['max_daily_rainfall'] = all_df['max_daily_rainfall'].abs()
    all_df['rainfall_intensity'] = all_df['rainfall_intensity'].abs()
    
    # 5. Save
    print_step(5, 5, "Saving dataset...")
    
    # Chọn cột output
    output_columns = [
        'latitude', 'longitude', 'landslide',
        'elevation', 'slope', 'aspect',
        'annual_precipitation', 'max_daily_rainfall', 'rainfall_intensity',
        'ndvi', 'distance_to_fault'
    ]
    
    output_df = all_df[output_columns].copy()
    output_df = output_df.dropna()
    
    output_df.to_csv(output_csv, index=False)
    
    print(f"\n  Dataset saved: {output_csv}")
    print(f"  Shape: {output_df.shape}")
    print(f"  Columns: {output_df.columns.tolist()}")
    print("\n  Landslide distribution:")
    print(f"    {output_df['landslide'].value_counts().to_dict()}")
    print("\n  Feature statistics:")
    print(output_df.describe().round(2).to_string())
    
    return output_df


# ============================================================
# 5. TẠO DATASET VỚI GEE
# ============================================================

def create_dataset_with_gee(output_csv='landslide_dataset.csv', hdx_csv=None):
    """
    Tạo dataset bằng Google Earth Engine.
    
    Yêu cầu:
    - Đăng ký GEE: https://earthengine.google.com/
    - pip install earthengine-api
    - ee.Authenticate() (chạy 1 lần)
    """
    try:
        import ee
    except ImportError:
        print("ERROR: earthengine-api not installed.")
        print("Run: pip install earthengine-api")
        return None
    
    # Khởi tạo GEE
    try:
        ee.Initialize()
        print("GEE initialized successfully!")
    except Exception as e:
        print(f"GEE init failed: {e}")
        print("Run: python -c \"import ee; ee.Authenticate()\"")
        return None
    
    print_header("TẠO DATASET VỚI GOOGLE EARTH ENGINE")
    
    # 1. Load ground truth
    print_step(1, 6, "Loading ground truth...")
    positive_df = load_ground_truth(hdx_csv)
    
    # Convert to ee.FeatureCollection
    features = []
    for _, row in positive_df.iterrows():
        point = ee.Geometry.Point([row['longitude'], row['latitude']])
        feature = ee.Feature(point, {
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'landslide': 1
        })
        features.append(feature)
    
    positive_fc = ee.FeatureCollection(features)
    n_positive = positive_fc.size().getInfo()
    print(f"  Positive samples: {n_positive}")
    
    # 2. Generate negative samples
    print_step(2, 6, "Generating negative samples...")
    bounds = positive_fc.geometry().bounds()
    random_points = ee.FeatureCollection.randomPoints(
        region=bounds,
        points=n_positive,
        seed=42
    )
    negative_fc = random_points.map(lambda f: f.set('landslide', 0))
    print(f"  Negative samples: {n_positive}")
    
    # 3. Merge
    all_points = positive_fc.merge(negative_fc)
    
    # 4. Extract terrain features (SRTM)
    print_step(3, 6, "Extracting terrain features (SRTM)...")
    srtm = ee.Image('USGS/SRTMGL1_003')
    terrain = ee.Terrain.products(srtm)
    
    def get_terrain(point):
        elev = srtm.reduceRegion(reducer=ee.Reducer.mean(), geometry=point.geometry(), scale=30).get('elevation')
        slope = terrain.select('slope').reduceRegion(reducer=ee.Reducer.mean(), geometry=point.geometry(), scale=30).get('slope')
        aspect = terrain.select('aspect').reduceRegion(reducer=ee.Reducer.mean(), geometry=point.geometry(), scale=30).get('aspect')
        return point.set({'elevation': elev, 'slope': slope, 'aspect': aspect})
    
    all_points = all_points.map(get_terrain)
    
    # 5. Extract precipitation (CHIRPS)
    print_step(4, 6, "Extracting precipitation (CHIRPS)...")
    chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
        .filterDate('2020-01-01', '2023-12-31') \
        .select('precipitation')
    
    annual_precip = chirps.sum().rename('annual_precipitation')
    max_daily = chirps.max().rename('max_daily_rainfall')
    mean_rainfall = chirps.mean().rename('rainfall_intensity')
    precip_img = annual_precip.addBands(max_daily).addBands(mean_rainfall)
    
    def get_precip(point):
        values = precip_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=point.geometry(), scale=5000)
        return point.set({
            'annual_precipitation': values.get('annual_precipitation'),
            'max_daily_rainfall': values.get('max_daily_rainfall'),
            'rainfall_intensity': values.get('rainfall_intensity')
        })
    
    all_points = all_points.map(get_precip)
    
    # 6. Extract NDVI (Sentinel-2)
    print_step(5, 6, "Extracting NDVI (Sentinel-2)...")
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterDate('2022-01-01', '2023-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .select(['B4', 'B8'])
    
    ndvi = s2.map(lambda img: img.normalizedDifference(['B8', 'B4']).rename('ndvi'))
    ndvi_mean = ndvi.mean().rename('ndvi')
    
    def get_ndvi(point):
        val = ndvi_mean.reduceRegion(reducer=ee.Reducer.mean(), geometry=point.geometry(), scale=100).get('ndvi')
        return point.set({'ndvi': val})
    
    all_points = all_points.map(get_ndvi)
    
    # 7. Export
    print_step(6, 6, "Exporting to CSV...")
    features_list = all_points.getInfo()['features']
    
    records = []
    for feat in features_list:
        props = feat['properties']
        coords = feat['geometry']['coordinates']
        records.append({
            'latitude': coords[1],
            'longitude': coords[0],
            'landslide': props.get('landslide', 0),
            'elevation': props.get('elevation'),
            'slope': props.get('slope'),
            'aspect': props.get('aspect'),
            'annual_precipitation': props.get('annual_precipitation'),
            'max_daily_rainfall': props.get('max_daily_rainfall'),
            'rainfall_intensity': props.get('rainfall_intensity'),
            'ndvi': props.get('ndvi'),
            'distance_to_fault': estimate_fault_distance(coords[1], coords[0]),
        })
    
    df = pd.DataFrame(records)
    df = df.dropna()
    df.to_csv(output_csv, index=False)
    
    print(f"\n  Dataset saved: {output_csv}")
    print(f"  Shape: {df.shape}")
    print("\n  Landslide distribution:")
    print(f"    {df['landslide'].value_counts().to_dict()}")
    
    return df


# ============================================================
# 6. TẠO DATASET SYNTHETIC (TEST)
# ============================================================

def create_dataset_synthetic(output_csv='landslide_dataset.csv', n_samples=2000):
    """
    Tạo dataset synthetic để test pipeline.
    Không cần API hay đăng ký.
    """
    print_header("TẠO DATASET SYNTHETIC (TEST)")
    
    np.random.seed(42)
    
    # Tạo vị trí ngẫu nhiên tại Việt Nam
    latitudes = np.random.uniform(10.0, 23.0, n_samples)
    longitudes = np.random.uniform(103.0, 110.0, n_samples)
    
    # Tạo features
    df = pd.DataFrame({
        'latitude': latitudes,
        'longitude': longitudes,
        'elevation': np.abs(np.random.normal(400, 250, n_samples)),
        'slope': np.abs(np.random.exponential(15, n_samples)),
        'aspect': np.random.uniform(0, 360, n_samples),
        'annual_precipitation': np.abs(np.random.normal(1800, 600, n_samples)),
        'max_daily_rainfall': np.abs(np.random.normal(80, 30, n_samples)),
        'rainfall_intensity': np.abs(np.random.normal(25, 10, n_samples)),
        'ndvi': np.random.uniform(0.1, 0.7, n_samples),
        'distance_to_fault': np.abs(np.random.exponential(5, n_samples)),
    })
    
    # Tạo label dựa trên risk factors
    risk = (
        (df['slope'] / 50) * 0.25 +
        (df['annual_precipitation'] / 3000) * 0.20 +
        (df['max_daily_rainfall'] / 150) * 0.15 +
        (1 / (df['distance_to_fault'] + 1)) * 0.20 +
        (1 - df['ndvi']) * 0.20
    )
    df['landslide'] = (risk + np.random.normal(0, 0.08, n_samples) > 0.45).astype(int)
    
    df.to_csv(output_csv, index=False)
    
    print(f"\n  Dataset saved: {output_csv}")
    print(f"  Shape: {df.shape}")
    print("\n  Landslide distribution:")
    print(f"    {df['landslide'].value_counts().to_dict()}")
    print("\n  Feature statistics:")
    print(df.describe().round(2).to_string())
    
    return df


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tạo dataset Landslide Susceptibility cho ML Training',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  # Test nhanh với synthetic data
  python create_dataset.py --mode synthetic --output dataset.csv

  # Tạo dataset thật với API miễn phí
  python create_dataset.py --mode api --output dataset.csv

  # Tạo dataset với file HDX
  python create_dataset.py --mode api --output dataset.csv --hdx hdx_data.csv

  # Dùng Google Earth Engine
  python create_dataset.py --mode gee --output dataset.csv
        """
    )
    
    parser.add_argument('--mode', type=str, default='synthetic',
                        choices=['synthetic', 'api', 'gee'],
                        help='Chế độ: synthetic (test), api (miễn phí), gee (Earth Engine)')
    parser.add_argument('--output', type=str, default='landslide_dataset.csv',
                        help='Đường dẫn file output CSV')
    parser.add_argument('--hdx', type=str, default=None,
                        help='Đường dẫn file CSV từ HDX/DesInventar')
    parser.add_argument('--no-meteostat', action='store_true',
                        help='Không dùng Meteostat API (chỉ dùng cho mode api)')
    
    args = parser.parse_args()
    
    print_header("TERRAALERT - LANDSLIDE DATASET GENERATOR")
    print(f"  Mode: {args.mode}")
    print(f"  Output: {args.output}")
    print(f"  HDX file: {args.hdx or 'None (using sample data)'}")
    
    if args.mode == 'synthetic':
        create_dataset_synthetic(args.output)
    
    elif args.mode == 'api':
        use_meteostat = not args.no_meteostat
        create_dataset_with_api(args.output, args.hdx, use_meteostat)
    
    elif args.mode == 'gee':
        create_dataset_with_gee(args.output, args.hdx)
    
    print_header("HOÀN THÀNH!")
    print(f"  File: {args.output}")
    print("  Bước tiếp theo: Upload file này lên Kaggle và chạy notebook training")
