# Chuyển đổi PDF sang Markdown bằng MiniMax-M3

Script này trích xuất văn bản từ một thư mục chứa các file PDF, sau đó sử dụng model MiniMax-M3 qua một API tương thích với cấu trúc của OpenAI để format lại văn bản thành dạng Markdown hoàn chỉnh. Dữ liệu đầu ra này cực kỳ tối ưu cho các hệ thống RAG.

## Tính năng

- Đọc file `.pdf` tự động bằng `PyMuPDF`.
- Giữ nguyên số liệu, cấu trúc bảng, danh sách.
- Nối các câu bị gãy vỡ (do lỗi đọc layout của PDF).
- Tự động tạo thư mục input/output.
- Hỗ trợ file `.env` để bảo mật API Key.

## Cài đặt

1. Đảm bảo bạn đã cài Python 3.8+ trên máy.
2. Cài đặt các thư viện yêu cầu:
```bash
pip install -r requirements.txt
```

## Cấu hình (Tùy chọn)

Bạn có thể tạo một file `.env` bằng cách đổi tên file `.env.example` thành `.env` và điền API Key thực tế của bạn vào. Nếu không dùng `.env`, bạn có thể sửa trực tiếp biến `API_KEY` trong file `main.py`.

```env
MINIMAX_API_KEY=your_real_api_key_here
MINIMAX_BASE_URL=https://api.tokenrouter.com/v1
```

## Sử dụng

Chạy script bằng lệnh sau:
```bash
python main.py
```

Lần chạy đầu tiên, script sẽ tự động tạo cấu trúc thư mục như sau:
```
scripts/pdf_to_md_minimax/
├── data/
│   ├── pdfs/       <-- (1) Bạn copy file .pdf vào đây
│   └── markdowns/  <-- (2) File .md kết quả sẽ nằm ở đây
├── main.py
...
```

1. Bạn chỉ cần thả các file PDF cần xử lý vào folder `data/pdfs`.
2. Chạy lại `python main.py`.
3. Kiểm tra kết quả trong thư mục `data/markdowns`.

## Lưu ý đối với file PDF dài
Nếu file PDF quá dài (chứa hàng trăm trang) vượt quá Context Window của model, hệ thống API có thể trả về lỗi. Trong trường hợp đó, bạn nên cắt nhỏ file PDF ra thành từng phần nhỏ (ví dụ 10-20 trang một phần) trước khi chạy.
