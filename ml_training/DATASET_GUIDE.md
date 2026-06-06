# Hướng Dẫn Tạo Dataset & Huấn luyện Mô hình Landslide Susceptibility

Tài liệu này hướng dẫn cách trích xuất dữ liệu, huấn luyện mô hình học máy (LSM - Landslide Susceptibility Mapping) cho hệ thống TerraAlert.

> [!IMPORTANT]
> **Dành cho Nghiên cứu Học thuật (Research Paper):** BẮT BUỘC sử dụng phương pháp **Google Earth Engine (GEE)** để trích xuất dữ liệu vệ tinh thực tế (SRTM DEM, Sentinel-2, CHIRPS) để đảm bảo độ chính xác và tính hợp lệ khoa học.
> 
> **Dành cho Chạy Demo Hệ Thống:** Có thể sử dụng chế độ `--mode api` (OpenTopoData + Meteostat) để tạo dữ liệu giả lập nhanh chóng mà không cần đăng ký tài khoản GEE.

---

## 1. Phương pháp Học thuật: Sử dụng Google Earth Engine (Khuyến nghị)

Phương pháp này dùng để thu thập dữ liệu không gian thực tế tại Việt Nam để xuất bản báo cáo.

### 1.1. Chuẩn bị tài khoản & Môi trường
1. Đăng ký tài khoản GEE tại: [https://earthengine.google.com/](https://earthengine.google.com/) (Duyệt từ 1-7 ngày).
2. Cài đặt thư viện Python:
```bash
pip install earthengine-api pandas numpy
```
3. Xác thực GEE trên máy:
```bash
python -c "import ee; ee.Authenticate()"
```

### 1.2. Chuẩn bị Ground Truth (Dữ liệu sạt lở thực tế)
Bạn cần tải tọa độ các vụ sạt lở lịch sử tại Việt Nam:
- **Nguồn:** [Humanitarian Data Exchange (HDX) - Vietnam Disasters](https://data.humdata.org/) hoặc [DesInventar Sendai](https://www.desinventar.net/).
- **Yêu cầu:** File CSV chứa tọa độ của các vụ sạt lở. Script đã được nâng cấp để tự động nhận diện các tên cột phổ biến (`Lat`, `Y`, `Vĩ độ`, `Longitude`, `X`, `Kinh độ`).

### 1.3. Trích xuất Dataset
```bash
cd ml_training/scripts
python create_dataset.py --mode gee --output dataset.csv --hdx path/to/hdx_landslide_vietnam.csv
```
*Dữ liệu sẽ chứa các đặc trưng thực tế từ SRTM (độ cao, độ dốc), Sentinel-2 (NDVI), CHIRPS (Lượng mưa).*

---

## 2. Phương pháp Demo: Sử dụng Public APIs (Nhanh, không cần duyệt)

Dành cho các bạn muốn build thử hệ thống ngay lập tức nhưng chưa có tài khoản GEE.

### 2.1. Cài đặt thư viện
```bash
pip install pandas numpy requests meteostat
```

### 2.2. Trích xuất Dataset
```bash
cd ml_training/scripts

# Tùy chọn 1: Dùng data sạt lở mẫu tích hợp sẵn (Không cần file HDX)
python create_dataset.py --mode api --output dataset.csv

# Tùy chọn 2: Dùng file HDX của bạn
python create_dataset.py --mode api --output dataset.csv --hdx path/to/hdx.csv
```
> [!NOTE]
> Chế độ này dùng **OpenTopoData API** để lấy độ cao và **Meteostat** để lấy lượng mưa. Một số chỉ số như Độ dốc (Slope) và Chỉ số thực vật (NDVI) sẽ được ước tính (estimate) một cách tương đối.

---

## 3. Huấn Luyện Mô Hình (Training)

Sau khi có file `dataset.csv`, bạn có thể huấn luyện mô hình.

### 3.1. Sử dụng Kaggle (Khuyến nghị để có GPU/RAM mạnh)
1. Vào [Kaggle](https://www.kaggle.com/), tạo Notebook mới.
2. Tab **Files** -> **Upload** -> Chọn file `dataset.csv`.
3. Tab **File** -> **Import Notebook** -> Chọn file `ml_training/landslide_susceptibility_training.ipynb`.
4. Click **Run All**.
5. Sau khi xong, tải các file mô hình ở thư mục `output/` bên phải.

### 3.2. Sử dụng Local (Jupyter Notebook)
1. Cài đặt: `pip install jupyterlab xgboost scikit-learn matplotlib seaborn`
2. Đảm bảo file `dataset.csv` nằm cùng thư mục với notebook.
3. Mở notebook và chạy tất cả các cell.

---

## 4. Tích hợp vào Hệ Thống TerraAlert

Sau khi huấn luyện thành công, copy 4 file sau vào backend:

```text
backend/app/slow_lane/ml/models/
├── lsm_xgboost_model.pkl          # Mô hình XGBoost (Chính)
├── lsm_random_forest_model.pkl    # Mô hình RF (Backup)
├── label_encoders.pkl             # Bộ mã hóa nhãn
└── model_metadata.json            # Thông tin metadata & metrics
```

Khởi động lại backend để hệ thống load mô hình mới:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Kiểm tra API:
```bash
curl http://localhost:8000/api/v1/slow-lane/map/susceptibility?lat=16.05&lon=108.20
```

---

## 5. Xử Lý Sự Cố (Troubleshooting)

- **Lỗi OpenTopoData API timeout trong chế độ `--mode api`**: Server API công cộng đôi khi bị quá tải. Script đã được cấu hình tự động thử lại (retry). Nếu vẫn thất bại, hãy đợi vài phút và chạy lại.
- **Meteostat không có dữ liệu trạm gần đó**: Sử dụng cờ `--no-meteostat` để hệ thống tự tạo dữ liệu lượng mưa mô phỏng: `python create_dataset.py --mode api --output dataset.csv --no-meteostat`.
- **Lỗi thiếu file CSV khi chạy Kaggle Notebook**: Cần đảm bảo file tải lên Kaggle có tên chính xác là `landslide_dataset.csv`. Notebook đã được thiết kế để tìm kiếm ở nhiều thư mục (`/kaggle/input/`, `/kaggle/working/`).
