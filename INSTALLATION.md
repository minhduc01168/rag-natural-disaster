# Hướng dẫn cài đặt TerraAlert

## Yêu cầu hệ thống

### Phần mềm cần cài đặt

| Phần mềm | Phiên bản | Bắt buộc | Ghi chú |
|----------|-----------|----------|---------|
| **Node.js** | ≥ 18.x (khuyến nghị 20.x) | ✅ | [Download](https://nodejs.org/) |
| **npm** | ≥ 9.x | ✅ | Comes with Node.js |
| **Python** | ≥ 3.9 | ✅ | [Download](https://python.org/) |
| **pip** | ≥ 23.x | ✅ | Comes with Python |
| **Docker** | ≥ 24.x | ✅ | [Download](https://docker.com/) |
| **Docker Compose** | ≥ 2.x | ✅ | Comes with Docker Desktop |
| **Git** | ≥ 2.x | ✅ | [Download](https://git-scm.com/) |

### Phần mềm tùy chọn

| Phần mềm | Mục đích |
|----------|----------|
| **VS Code** | Code editor |
| **Postman** | Test API |
| **pgAdmin** | Quản lý PostgreSQL |

---

## Cài đặt chi tiết

### 1. Cài đặt Node.js và npm

**Windows:**
1. Tải installer từ https://nodejs.org/
2. Chạy installer, chọn phiên bản LTS
3. Verify:
```bash
node --version  # Should be v18+ or v20+
npm --version   # Should be 9+
```

**macOS:**
```bash
# Using Homebrew
brew install node@20
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Cài đặt Python

**Windows:**
1. Tải installer từ https://python.org/
2. Chọn "Add Python to PATH" khi cài đặt
3. Verify:
```bash
python --version  # Should be 3.9+
pip --version
```

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 3. Cài đặt Docker

**Windows/macOS:**
1. Tải Docker Desktop từ https://docker.com/
2. Cài đặt và khởi động
3. Verify:
```bash
docker --version
docker compose version
```

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

---

## Cài đặt dự án

### 1. Clone repository
```bash
git clone <repository-url>
cd rag-natural-disaster
```

### 2. Cài đặt Frontend
```bash
cd frontend
npm install
```

### 3. Cài đặt Backend
```bash
cd ../backend

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Cấu hình Environment

**Frontend:**
```bash
cd frontend
cp .env.example .env
# Edit .env nếu cần
```

**Backend:**
```bash
cd backend
cp .env.example .env
# Edit .env với các giá trị thực tế
```

---

## Chạy ứng dụng

### Cách 1: Chạy riêng lẻ (Development)

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Cách 2: Chạy với Docker Compose (Production-like)

```bash
# Từ thư mục root
docker compose up -d
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- ChromaDB: localhost:8001

Dừng services:
```bash
docker compose down
```

Xóa volumes (reset data):
```bash
docker compose down -v
```

---

## Chạy Tests

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

---

## Troubleshooting

### Lỗi: Node version mismatch
```bash
# Sử dụng nvm để quản lý nhiều phiên bản Node
# Windows: sử dụng nvm-windows
# macOS/Linux:
nvm install 20
nvm use 20
```

### Lỗi: Python pip permission
```bash
# Sử dụng --user flag
pip install --user -r requirements.txt

# Hoặc tạo virtual environment
python -m venv venv
source venv/bin/activate  # hoặc venv\Scripts\activate trên Windows
```

### Lỗi: Docker permission denied
```bash
# Linux: thêm user vào docker group
sudo usermod -aG docker $USER
# Đăng nhập lại sau khi chạy lệnh trên
```

### Lỗi: Port already in use
```bash
# Tìm process đang sử dụng port
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Kill process hoặc thay đổi port trong .env
```

---

## API Endpoints

### Fast Lane (Real-time)
- `POST /api/v1/fast-lane/sos` - Gửi tín hiệu SOS
- `GET /api/v1/fast-lane/weather/{lat}/{lon}` - Lấy thời tiết
- `GET /api/v1/fast-lane/alerts` - Danh sách cảnh báo

### Slow Lane (AI/ML)
- `POST /api/v1/slow-lane/chat` - Chat với TerraBot
- `GET /api/v1/slow-lane/map/susceptibility` - Bản đồ nhạy cảm sạt lở
- `GET /api/v1/slow-lane/data/gis` - Dữ liệu GIS

### System
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

---

## Lưu ý quan trọng

1. **Node version**: Dự án hoạt động tốt nhất với Node 20.x. Node 18.x vẫn chạy được nhưng có thể có warnings.

2. **Environment Variables**: KHÔNG commit file `.env` với giá trị thật. Chỉ commit `.env.example`.

3. **Docker**: Cần cài đặt Docker Desktop để chạy với Docker Compose.

4. **API Keys**: Cần đăng ký và cấu hình các API keys:
   - Meteostat API (miễn phí): https://rapidapi.com/meteostat/api/meteostat/
   - Gemini API: https://makersuite.google.com/
   - Groq API: https://console.groq.com/

5. **PostgreSQL Extensions**: Cần cài PostGIS extension cho GIS features (sẽ cần trong Epic 4).
