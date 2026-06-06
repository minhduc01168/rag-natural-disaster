# Hướng Dẫn Chạy Toàn Bộ Pipeline ML Trên Kaggle

Tài liệu này là hướng dẫn **"cầm tay chỉ việc"** từ bước tạo dữ liệu đến lúc có mô hình hoàn chỉnh để tích hợp vào hệ thống TerraAlert sử dụng nền tảng Kaggle (nền tảng GPU/CPU đám mây miễn phí của Google).

---

## BƯỚC 1: TẠO DATASET TỪ DỮ LIỆU NASA

Do Kaggle yêu cầu một bộ dữ liệu đã được xử lý (Dataset) để đẩy vào Notebook, bạn cần phải tạo ra file `dataset.csv` chứa thông tin sạt lở, độ cao, lượng mưa trước.

1. **Tải file gốc:** Tải dữ liệu các vụ sạt lở toàn cầu (hoặc lọc riêng Việt Nam) tại link này: [NASA Global Landslide Catalog (Kaggle)](https://www.kaggle.com/datasets/nasa/landslide-events). Đổi tên file thành `nasa_landslides.csv`.
2. **Chép file gốc vào thư mục code:** Chép `nasa_landslides.csv` vào thư mục `ml_training/scripts/` trên máy tính của bạn.
3. **Chạy script tạo features:** Mở Terminal/PowerShell tại thư mục `rag-natural-disaster` và chạy lệnh sau (Script đã được tối ưu để tự động tìm cột tọa độ của NASA):
   ```bash
   python ml_training/scripts/create_dataset.py --mode api --output dataset.csv --hdx ml_training/scripts/nasa_landslides.csv
   ```
4. **Nhận kết quả:** Sau khoảng vài chục phút, bạn sẽ có file `dataset.csv` chứa đầy đủ hàng ngàn dòng dữ liệu (bao gồm cả các điểm tạo giả lập không sạt lở).

---

## BƯỚC 2: KHỞI TẠO MÔI TRƯỜNG KAGGLE

Kaggle giúp máy tính của bạn không bị treo khi huấn luyện các mô hình lớn.

1. **Đăng nhập:** Truy cập [Kaggle](https://www.kaggle.com/) và đăng nhập (bằng tài khoản Google).
2. **Tạo Kaggle Dataset:**
   - Vào menu trái -> **Datasets** -> **New Dataset**.
   - Kéo thả file `dataset.csv` vừa tạo ở Bước 1 vào. Đặt tên là `TerraAlert_Dataset_v1`.
   - Nhấn **Create**.
3. **Tạo Notebook mới:**
   - Nhấn vào avatar/menu trái -> **Code** -> **New Notebook**.
   - Đổi tên Notebook trên cùng bên trái thành `TerraAlert-ML-Training`.

---

## BƯỚC 3: ĐƯA CODE LÊN VÀ TRAINING

1. **Import code của dự án:**
   - Trong Notebook Kaggle, nhìn lên menu ngang trên cùng -> Chọn **File** -> **Import Notebook**.
   - Chọn file `ml_training/landslide_susceptibility_training.ipynb` từ máy tính của bạn để tải lên.
2. **Thêm Dataset vào Notebook:**
   - Ở cột bên phải (bảng Data/Input), nhấn nút **Add Input** (hoặc dấu `+`).
   - Chọn tab **Your Datasets** -> Tìm `TerraAlert_Dataset_v1` -> Nhấn dấu `+` để Add.
3. **Training Mô hình:**
   - Nhấn nút **Run All** ở thanh menu trên cùng.
   - Thư giãn và đợi! Kaggle sẽ chạy qua các bước: Làm sạch dữ liệu -> Phân tích (Vẽ biểu đồ) -> Khởi tạo thuật toán Random Forest & XGBoost -> K-Fold Cross Validation.
   - Code đã được thiết lập để **tự động dò tìm** file `dataset.csv` trong môi trường Kaggle, bạn không cần sửa đường dẫn.

---

## BƯỚC 4: LẤY KẾT QUẢ VÀ TÍCH HỢP VÀO TERRAALERT

Khi Notebook chạy tới cell cuối cùng, nó sẽ báo "Models saved successfully!".

1. Nhìn sang cột bên phải (bảng **Output**), tìm thư mục `/kaggle/working/output/`.
2. Bạn sẽ thấy 4 file thành quả:
   - `lsm_xgboost_model.pkl`
   - `lsm_random_forest_model.pkl`
   - `label_encoders.pkl`
   - `model_metadata.json`
3. Nhấn **Download** từng file về máy tính.
4. **Tích hợp:** Chép 4 file này đè vào thư mục `backend/app/slow_lane/ml/models/` của dự án TerraAlert.
5. Khởi động lại FastAPI Backend. Hệ thống của bạn đã được nâng cấp với "bộ não" mới được huấn luyện từ hàng ngàn dữ liệu của NASA!

> **Chúc bạn huấn luyện mô hình thành công!** 🚀
