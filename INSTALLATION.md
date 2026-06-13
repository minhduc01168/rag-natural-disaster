# Hướng dẫn khởi chạy hệ thống TerraAlert (Agentic RAG)

Dự án TerraAlert đã được tối giản hóa nhờ kiến trúc Agentic RAG mới. Bạn không cần cài đặt các Database nặng nề như PostgreSQL hay Redis nữa.

## 1. Yêu cầu hệ thống tối thiểu

- **Docker Desktop** (hoặc Docker Engine + Docker Compose) đã được cài đặt và đang chạy.
- **Git** (để clone mã nguồn).
- **Node.js** và **Python 3.11+** (nếu muốn chạy thủ công không qua Docker).

---

## 2. Hướng dẫn cài đặt công cụ cho từng Hệ điều hành

### 🪟 Trên Windows
- **Git:** Tải và cài đặt Git từ [git-scm.com/download/win](https://git-scm.com/download/win) hoặc mở PowerShell và chạy lệnh: `winget install --id Git.Git -e --source winget`
- **Docker:** Tải và cài đặt **Docker Desktop** tại [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/). *(Khuyến nghị bật tính năng WSL 2 backend trong lúc cài đặt để chạy mượt mà).*

### 🍎 Trên macOS
- **Git:** Mở Terminal và chạy lệnh: `xcode-select --install` hoặc cài qua Homebrew: `brew install git`
- **Docker:** Tải Docker Desktop cho Mac tại [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) hoặc cài qua Homebrew: `brew install --cask docker`

### 🐧 Trên Ubuntu / Linux
Mở Terminal và lần lượt chạy các lệnh sau để cài đặt Git và Docker:
```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt Git
sudo apt install git -y

# Cài đặt Docker và Docker Compose plugin
sudo apt install docker.io docker-compose-v2 -y

# Thêm user hiện tại vào group docker để không cần gõ sudo mỗi khi dùng docker
sudo usermod -aG docker $USER
newgrp docker
```

---

## 3. Thiết lập môi trường

Đầu tiên, tải mã nguồn về máy:

```bash
git clone https://github.com/minhduc01168/rag-natural-disaster.git
cd rag-natural-disaster
```

Tiếp theo, bạn cần cấp khóa API cho AI (Google Gemini):

1. Mở thư mục `backend/`
2. Tạo file `.env` bằng cách copy từ file mẫu:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Mở file `backend/.env` bằng trình soạn thảo (Notepad/VSCode) và điền key của bạn vào:
   ```env
   # Điền API Key lấy từ: https://aistudio.google.com/
   GEMINI_API_KEY=AIzaSyYourSecretKeyHere...
   ```

## 4. Khởi chạy bằng Docker Compose (Khuyến nghị)

Cách đơn giản và sạch sẽ nhất là dùng Docker để khởi chạy toàn bộ hệ thống (Frontend, Backend, ChromaDB) chỉ bằng 1 lệnh.

Mở Terminal (hoặc Powershell) tại thư mục gốc `rag-natural-disaster` và chạy:

```bash
docker-compose build
docker-compose up -d
```

> **Lưu ý:** Lần chạy đầu tiên sẽ tốn khoảng 3-5 phút để tải các Images cần thiết (Python, Node, Chroma) và biên dịch.

Kiểm tra trạng thái các container:
```bash
docker-compose ps
```

## 5. Truy cập hệ thống

Sau khi Docker báo `Started`, bạn có thể truy cập:

- 🌐 **Giao diện Web (TerraBot Chat):** [http://localhost:3000](http://localhost:3000)
- ⚙️ **API Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- 🗄️ **ChromaDB (Vector Database):** Đang chạy ngầm ở port `8001`

---

## 6. (Tùy chọn) Chạy thủ công không dùng Docker

Nếu bạn muốn chạy trực tiếp trên máy để code/debug:

**Bước 1: Chạy Backend (FastAPI)**
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # (Dùng trên Windows)
# source venv/bin/activate # (Dùng trên Mac/Linux)

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Bước 2: Chạy Frontend (React)**
Mở một cửa sổ Terminal mới:
```bash
cd frontend
npm install
npm run dev
```

Truy cập `http://localhost:5173` để dùng giao diện dev.

---

## 7. Lệnh dọn dẹp thường dùng (Docker)

Để tắt hệ thống:
```bash
docker-compose down
```

Để tắt và xóa sạch dữ liệu (Reset ChromaDB vector):
```bash
docker-compose down -v
```
