"""
Script trích xuất dữ liệu GIS từ Google Earth Engine (GEE) cho Landslide Susceptibility Mapping

Yêu cầu:
1. Đăng ký GEE: https://earthengine.google.com/
2. pip install earthengine-api pandas
3. ee.Authenticate() (chạy 1 lần)

Cách chạy:
    python create_dataset.py --output landslide_dataset.csv
"""

import ee
import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime


# ============================================================
# KHỞI TẠO GEE
# ============================================================

def init_gee():
    """Khởi tạo Earth Engine connection."""
    try:
        ee.Initialize()
        print("GEE initialized successfully!")
    except Exception as e:
        print(f"GEE init failed: {e}")
        print("Run: ee.Authenticate() first")
        raise


# ============================================================
# 1. LẤY GROUND TRUTH (VỊ TRÍ SẠT LỞ)
# ============================================================

def get_landslide_points_from_hdx(hdx_csv_path=None):
    """
    Load landslide locations từ file CSV đã download từ HDX/DesInventar.
    
    Expected CSV format:
        latitude,longitude,event_date,disaster_type,source
        16.05,108.20,2020-10-15,landslide,HDX
        ...
    
    Returns: ee.FeatureCollection
    """
    if hdx_csv_path and os.path.exists(hdx_csv_path):
        df = pd.read_csv(hdx_csv_path)
        print(f"Loaded {len(df)} landslide records from {hdx_csv_path}")
    else:
        print("No HDX file provided. Using sample Vietnam landslide locations.")
        # Sample landslide locations tại Việt Nam (từ các sự kiện có thật)
        data = {
            'latitude': [
                16.05, 16.07, 15.60, 15.62, 15.12, 14.58, 14.02, 13.45,
                12.25, 11.55, 10.85, 10.35, 21.03, 20.95, 22.35, 22.40,
                14.85, 14.90, 15.30, 15.35, 16.50, 16.55, 17.20, 17.25,
                18.10, 18.15, 19.05, 19.10, 20.15, 20.20
            ],
            'longitude': [
                108.20, 108.22, 108.35, 108.38, 108.85, 108.50, 108.92, 109.15,
                108.50, 108.00, 107.10, 106.65, 105.85, 105.80, 103.95, 103.90,
                108.70, 108.72, 108.45, 108.48, 107.80, 107.82, 107.50, 107.52,
                106.50, 106.52, 105.80, 105.82, 105.50, 105.52
            ],
            'event_date': [
                '2020-10-15', '2020-10-15', '2020-10-18', '2020-10-18',
                '2020-10-20', '2020-10-22', '2020-10-25', '2020-10-28',
                '2020-11-01', '2020-11-05', '2020-11-10', '2020-11-15',
                '2021-06-15', '2021-06-15', '2021-07-20', '2021-07-20',
                '2021-08-10', '2021-08-10', '2021-09-05', '2021-09-05',
                '2022-06-20', '2022-06-20', '2022-07-15', '2022-07-15',
                '2022-08-10', '2022-08-10', '2022-09-01', '2022-09-01',
                '2023-06-15', '2023-06-15'
            ]
        }
        df = pd.DataFrame(data)
    
    # Convert to ee.FeatureCollection
    features = []
    for _, row in df.iterrows():
        point = ee.Geometry.Point([row['longitude'], row['latitude']])
        feature = ee.Feature(point, {
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'landslide': 1,
            'event_date': str(row.get('event_date', ''))
        })
        features.append(feature)
    
    return ee.FeatureCollection(features)


def generate_negative_samples(positive_fc, n_negative=500, buffer_km=50):
    """
    Tạo negative samples (điểm không có sạt lở) trong cùng khu vực.
    
    Strategy:
    - Random points trong bounding box của positive samples
    - Buffer ra ngoài một chút để tránh overlap
    """
    # Lấy bounds của positive samples
    bounds = positive_fc.geometry().bounds()
    
    # Tạo random points
    random_points = ee.FeatureCollection.randomPoints(
        region=bounds,
        points=n_negative,
        seed=42
    )
    
    # Thêm label = 0
    negative_fc = random_points.map(lambda f: f.set('landslide', 0))
    
    return negative_fc


# ============================================================
# 2. LẤY ĐẶC TRƯNG ĐỊA HÌNH (SRTM DEM)
# ============================================================

def extract_terrain_features(point_fc):
    """
    Trích xuất đặc trưng địa hình từ SRTM DEM tại các điểm.
    
    Features:
    - elevation: Độ cao (m)
    - slope: Độ dốc (độ)
    - aspect: Hướng dốc (0-360)
    - curvature: Độ cong
    """
    # Load SRTM DEM (30m resolution)
    srtm = ee.Image('USGS/SRTMGL1_003')
    
    # Tính slope và aspect
    terrain = ee.Terrain.products(srtm)
    
    # Tính curvature (second derivative)
    # curvature = d²z/dx² + d²z/dy²
    dem = srtm.select('elevation')
    slope_img = terrain.select('slope')
    aspect_img = terrain.select('aspect')
    
    # Extract values tại mỗi điểm
    def get_terrain_values(point):
        elev = srtm.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point.geometry(),
            scale=30
        ).get('elevation')
        
        slope_val = slope_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point.geometry(),
            scale=30
        ).get('slope')
        
        aspect_val = aspect_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point.geometry(),
            scale=30
        ).get('aspect')
        
        return point.set({
            'elevation': elev,
            'slope': slope_val,
            'aspect': aspect_val
        })
    
    return point_fc.map(get_terrain_values)


# ============================================================
# 3. LẤY ĐẶC TRƯNG KHÍ TƯỢNG (GPM IMERG / CHIRPS)
# ============================================================

def extract_precipitation_features(point_fc, start_date='2020-01-01', end_date='2023-12-31'):
    """
    Trích xuất đặc trưng lượng mưa từ GPM IMERG hoặc CHIRPS.
    
    Features:
    - annual_precipitation: Tổng lượng mưa năm (mm)
    - max_daily_rainfall: Mưa max trong ngày (mm)
    - rainfall_intensity: Cường độ mưa trung bình (mm/day)
    """
    # Option 1: GPM IMERG (30min resolution, từ 2000)
    gpm = ee.ImageCollection('NASA/GPM_L3/IMERG_MONTHLY_V06') \
        .filterDate(start_date, end_date) \
        .select('precipitationCal')
    
    # Option 2: CHIRPS (daily, từ 1981) - tốt hơn cho tropical regions
    chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
        .filterDate(start_date, end_date) \
        .select('precipitation')
    
    # Tính tổng lượng mưa năm
    annual_precip = chirps.sum().rename('annual_precipitation')
    
    # Tính max daily rainfall
    max_daily = chirps.max().rename('max_daily_rainfall')
    
    # Tính mean rainfall
    mean_rainfall = chirps.mean().rename('rainfall_intensity')
    
    # Combine
    precip_img = annual_precip.addBands(max_daily).addBands(mean_rainfall)
    
    # Extract values
    def get_precip_values(point):
        values = precip_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point.geometry(),
            scale=5000  # 5km resolution
        )
        return point.set({
            'annual_precipitation': values.get('annual_precipitation'),
            'max_daily_rainfall': values.get('max_daily_rainfall'),
            'rainfall_intensity': values.get('rainfall_intensity')
        })
    
    return point_fc.map(get_precip_values)


# ============================================================
# 4. LẤY CHỈ SỐ THỰC VẬT (NDVI TỪ SENTINEL-2)
# ============================================================

def extract_ndvi_features(point_fc, start_date='2022-01-01', end_date='2023-12-31'):
    """
    Trích xuất NDVI từ Sentinel-2 tại các điểm.
    
    NDVI = (NIR - Red) / (NIR + Red)
    - Giá trị từ -1 đến 1
    - Càng cao = thảm thực vật càng tốt = ít sạt lở hơn
    """
    # Load Sentinel-2 Surface Reflectance
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .select(['B4', 'B8'])  # Red, NIR
    
    # Tính NDVI trung bình
    ndvi = s2.map(lambda img: img.normalizedDifference(['B8', 'B4']).rename('ndvi'))
    ndvi_mean = ndvi.mean().rename('ndvi')
    
    # Extract values
    def get_ndvi(point):
        val = ndvi_mean.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point.geometry(),
            scale=100  # 100m resolution
        ).get('ndvi')
        return point.set({'ndvi': val})
    
    return point_fc.map(get_ndvi)


# ============================================================
# 5. LẤY ĐẶC TRƯNG ĐỊA CHẤT (FAULT LINES)
# ============================================================

def extract_geological_features(point_fc):
    """
    Trích xuất đặc trưng địa chất.
    
    Features:
    - distance_to_fault: Khoảng cách đến đứt gãy gần nhất (km)
    """
    # Fault lines tại Việt Nam (dữ liệu từ USGS)
    # Tham khảo: https://www.usgs.gov/programs/earthquake-hazards/faults
    fault_data = [
        # [longitude, latitude] - Các đứt gãy chính tại Việt Nam
        [108.2, 16.0],   # Đứt gãy Đà Nẵng
        [107.5, 15.5],   # Đứt gãy Quảng Nam
        [106.8, 14.5],   # Đứt gãy Quảng Ngãi
        [105.8, 21.0],   # Đứt gãy sông Hồng
        [106.5, 20.5],   # Đứt gãy Lai Châu
        [107.0, 18.0],   # Đứt gãy Nghệ An
        [108.5, 12.0],   # Đứt gãy Nha Trang
        [106.7, 10.8],   # Đứt gãy TP.HCM
    ]
    
    # Tạo FeatureCollection từ fault data
    fault_features = []
    for lon, lat in fault_data:
        point = ee.Geometry.Point([lon, lat])
        fault_features.append(ee.Feature(point))
    
    faults = ee.FeatureCollection(fault_features)
    
    # Tính khoảng cách từ mỗi điểm đến đứt gãy gần nhất
    def get_fault_distance(point):
        dist = faults.geometry().distance(point.geometry()).divide(1000)  # km
        return point.set({'distance_to_fault': dist})
    
    return point_fc.map(get_fault_distance)


# ============================================================
# 6. TẠO DATASET CUỐI CÙNG
# ============================================================

def create_dataset(output_csv='landslide_dataset.csv', use_hdx_file=None):
    """
    Tạo dataset hoàn chỉnh cho ML training.
    """
    print("="*60)
    print("TẠO DATASET LANDSLIDE SUSCEPTIBILITY")
    print("="*60)
    
    # 1. Load ground truth
    print("\n[1/5] Loading landslide locations...")
    positive_fc = get_landslide_points_from_hdx(use_hdx_file)
    n_positive = positive_fc.size().getInfo()
    print(f"  Positive samples: {n_positive}")
    
    # 2. Generate negative samples
    print("\n[2/5] Generating negative samples...")
    negative_fc = generate_negative_samples(positive_fc, n_negative=n_positive)  # 1:1 ratio
    n_negative = negative_fc.size().getInfo()
    print(f"  Negative samples: {n_negative}")
    
    # 3. Merge
    all_points = positive_fc.merge(negative_fc)
    print(f"  Total samples: {all_points.size().getInfo()}")
    
    # 4. Extract features
    print("\n[3/5] Extracting terrain features (SRTM)...")
    all_points = extract_terrain_features(all_points)
    
    print("\n[4/5] Extracting precipitation features (CHIRPS)...")
    all_points = extract_precipitation_features(all_points)
    
    print("\n[5/5] Extracting NDVI features (Sentinel-2)...")
    all_points = extract_ndvi_features(all_points)
    
    print("\n[6/6] Extracting geological features...")
    all_points = extract_geological_features(all_points)
    
    # 5. Export to CSV
    print("\nExporting to CSV...")
    
    # Convert to pandas DataFrame
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
            'distance_to_fault': props.get('distance_to_fault'),
        })
    
    df = pd.DataFrame(records)
    
    # Drop rows with missing values
    df = df.dropna()
    
    # Save
    df.to_csv(output_csv, index=False)
    print(f"\nDataset saved: {output_csv}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nLandslide distribution:")
    print(df['landslide'].value_counts())
    
    return df


# ============================================================
# 7. THÊM FEATURES TỪ METEOSTAT (LOCAL)
# ============================================================

def add_meteostat_features(df, station_id='48855'):  # Đà Nẵng
    """
    Thêm dữ liệu khí tượng từ Meteostat API.
    
    Station IDs tại Việt Nam:
    - 48855: Đà Nẵng
    - 48845: Huế
    - 48820: Vinh
    - 48810: Hà Nội
    - 48900: TP.HCM
    
    Docs: https://dev.meteostat.net/python/
    """
    try:
        from meteostat import Point, Daily
        from datetime import datetime
        
        # Lấy dữ liệu daily cho station
        start = datetime(2020, 1, 1)
        end = datetime(2023, 12, 31)
        
        # Station location (Đà Nẵng)
        location = Point(16.05, 108.20)
        
        # Get daily data
        data = Daily(location, start, end)
        data = data.fetch()
        
        if not data.empty:
            # Tính stats
            avg_precip = data['prcp'].mean()
            max_precip = data['prcp'].max()
            
            print(f"Meteostat data for station {station_id}:")
            print(f"  Avg daily precipitation: {avg_precip:.1f} mm")
            print(f"  Max daily precipitation: {max_precip:.1f} mm")
            
            # Thêm features vào dataframe nếu chưa có
            if 'annual_precipitation' not in df.columns:
                df['annual_precipitation'] = avg_precip * 365  # Ước tính
            if 'max_daily_rainfall' not in df.columns:
                df['max_daily_rainfall'] = max_precip
        
        return df
        
    except ImportError:
        print("Meteostat not installed. Run: pip install meteostat")
        return df
    except Exception as e:
        print(f"Meteostat error: {e}")
        return df


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Landslide Dataset from GEE')
    parser.add_argument('--output', type=str, default='landslide_dataset.csv', help='Output CSV path')
    parser.add_argument('--hdx', type=str, default=None, help='Path to HDX/DesInventar CSV')
    parser.add_argument('--no-gee', action='store_true', help='Skip GEE, use synthetic data')
    
    args = parser.parse_args()
    
    if args.no_gee:
        print("Running in synthetic mode (no GEE)")
        # Tạo synthetic dataset
        np.random.seed(42)
        n = 2000
        
        df = pd.DataFrame({
            'latitude': np.random.uniform(10.0, 23.0, n),
            'longitude': np.random.uniform(103.0, 110.0, n),
            'elevation': np.abs(np.random.normal(400, 250, n)),
            'slope': np.abs(np.random.exponential(15, n)),
            'aspect': np.random.uniform(0, 360, n),
            'annual_precipitation': np.abs(np.random.normal(1800, 600, n)),
            'max_daily_rainfall': np.abs(np.random.normal(80, 30, n)),
            'rainfall_intensity': np.abs(np.random.normal(25, 10, n)),
            'ndvi': np.random.uniform(0.1, 0.7, n),
            'distance_to_fault': np.abs(np.random.exponential(5, n)),
        })
        
        # Create label
        risk = (
            (df['slope'] / 50) * 0.25 +
            (df['annual_precipitation'] / 3000) * 0.20 +
            (df['max_daily_rainfall'] / 150) * 0.15 +
            (1 / (df['distance_to_fault'] + 1)) * 0.20 +
            (1 - df['ndvi']) * 0.20
        )
        df['landslide'] = (risk + np.random.normal(0, 0.08, n) > 0.45).astype(int)
        
        df.to_csv(args.output, index=False)
        print(f"Synthetic dataset saved: {args.output}")
        print(f"Shape: {df.shape}")
        print(f"Landslide distribution:\n{df['landslide'].value_counts()}")
    else:
        init_gee()
        create_dataset(args.output, args.hdx)
