# Hướng Dẫn Chạy Hệ Thống TerraAlert Cục Bộ (Bao Gồm Model Embedding)

Tài liệu này hướng dẫn chi tiết cách chạy toàn bộ hệ thống TerraAlert trên máy cá nhân, đặc biệt đi sâu vào phần cấu hình và chạy **Embedding Service** dùng cho Agentic RAG.

## Kiến Trúc Hệ Thống Hiện Tại
Hệ thống gồm 3 thành phần chính:
1. **Frontend (React/Vite):** Giao diện người dùng (Cổng mặc định: `3000` hoặc `5173`).
2. **Backend (FastAPI):** Chứa Core RAG, Fast Lane (SOS) và Slow Lane (Chat). (Cổng mặc định: `8000`).
3. **Embedding Service (FastAPI + SentenceTransformers):** Microservice độc lập chạy model `microsoft/harrier-oss-v1-0.6b` để vector hóa văn bản. (Cổng mặc định: `8001`).

---

## 1. Yêu Cầu Cài Đặt Ban Đầu

- **Python 3.10+** (Khuyên dùng Python 3.11).
- **Node.js 18+** (Cho Frontend).
- **Git**.
- **Docker & Docker Compose** (Nếu muốn chạy dễ dàng bằng Container).

---

## 2. Thiết Lập API Key (Bắt Buộc)

Bạn cần Google Gemini API Key để Backend có thể sử dụng LLM.
1. Lấy API Key tại: [Google AI Studio](https://aistudio.google.com/)
2. Trỏ vào thư mục `backend/` và tạo file `.env`:
   ```bash
   cd backend
   cp .env.example .env
   ```
3. Mở file `.env` và thêm:
   ```env
   GEMINI_API_KEY=AIzaSy_YOUR_API_KEY_HERE
   ```

---

## 3. Cách 1: Chạy Tự Động Bằng Docker (Khuyến Nghị Nhất)

Đây là cách dễ nhất để chạy toàn bộ hệ thống từ A-Z mà không cần setup môi trường thủ công.

Tại thư mục gốc dự án, chạy:
```bash
docker-compose build
docker-compose up -d
```

**Quá trình này sẽ thực hiện:**
- Kéo image Python và cài đặt thư viện cho Backend.
- Tải model `microsoft/harrier-oss-v1-0.6b` nặng khoảng vài GB về máy lưu vào container `embedding_service`.
- Khởi tạo ChromaDB (được nhúng sẵn trong backend hoặc chạy độc lập tuỳ kiến trúc docker-compose).
- Build Frontend React.

Kiểm tra log của Embedding Service để xem model đã tải xong chưa:
```bash
docker-compose logs -f embedding_service
```
*(Đợi khi nào thấy dòng `Model loaded successfully.` là đã sẵn sàng)*.

---

## 4. Cách 2: Chạy Thủ Công (Dành Cho Developer / Debugging)

Nếu bạn muốn chạy riêng rẽ từng Service để code hoặc kiểm tra luồng RAG.

### 4.1. Khởi chạy Embedding Service
Service này cần tải model `sentence-transformers` về, lần đầu chạy sẽ tốn thời gian.

```bash
cd embedding_service

# 1. Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate  # Trên Mac/Linux
# venv\Scripts\activate   # Trên Windows

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Chạy service
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
*Lưu ý: Lần đầu tiên chạy, HuggingFace Hub sẽ tự động tải model `microsoft/harrier-oss-v1-0.6b` về thư mục cache cục bộ (thường là `~/.cache/huggingface/hub`). Hãy kiên nhẫn đợi.*

Kiểm tra Embedding API: http://localhost:8001/docs

### 4.2. Khởi chạy Backend FastAPI
Mở một Terminal MỚI:

```bash
cd backend

# 1. Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate  # Trên Mac/Linux
# venv\Scripts\activate   # Trên Windows

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Chạy backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Kiểm tra Backend API: http://localhost:8000/docs

### 4.3. Khởi chạy Frontend
Mở một Terminal MỚI:

```bash
cd frontend

# Cài đặt dependency
npm install

# Khởi chạy server phát triển
npm run dev
```
Truy cập Frontend tại: http://localhost:5173 (hoặc cổng được Vite cung cấp).

---

## 5. Chạy Automated Tests (E2E)
Chúng tôi đã viết sẵn các kịch bản kiểm thử E2E tự động tại `backend/tests/test_e2e.py`.
Để kiểm tra xem hệ thống đã hoạt động trơn tru chưa:

1. Đảm bảo cả `Backend` và `Embedding Service` đều đang chạy.
2. Mở terminal tại thư mục `backend/`:
   ```bash
   source venv/bin/activate
   pip install pytest requests
   pytest tests/test_e2e.py -v
   ```
Kết quả sẽ trả về các trạng thái `PASSED` nếu tất cả API SOS, Alert, Chat và Embedding đều phản hồi chính xác.
