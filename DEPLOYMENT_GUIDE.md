# Hướng Dẫn Vận Hành & Triển Khai Hệ Thống TERRA (Local & Server Port 3000)

Tài liệu này hướng dẫn chi tiết cách chạy hệ thống **TERRA (Hệ thống Hỗ trợ Ra Quyết định Phòng Chống Thiên Tai Miền Núi)** trên môi trường cục bộ (Local Development) và triển khai trên máy chủ thực tế (Production Server) với cổng truy cập giao diện là **Port 3000**, kèm theo cẩm nang đầy đủ về **cách mở Port trên tường lửa (Firewall) và các nền tảng Cloud**.

---

## 1. Tổng Quan Kiến Trúc Mạng & Cổng Dịch Vụ (Port Architecture)

Hệ thống được thiết kế theo mô hình vi dịch vụ container hóa (Docker):

| Dịch vụ | Port Nội bộ (Container) | Port Công khai (Host Server) | Mục đích & Giao thức |
| :--- | :---: | :---: | :--- |
| **Frontend (Web App)** | `80` | **`3000`** | Giao diện React/Vite, bản đồ GIS, Chatbot cứu nạn (Nginx Reverse Proxy) |
| **Backend (FastAPI)** | `8000` | `8000` | Core API, RAG Engine, Multi-Agent, Auth, Fast-lane cảnh báo |
| **ChromaDB** | `8000` | `8001` | Vector Database lưu trữ embedding tri thức thiên tai |
| **Embedding Service** | `8002` | `8002` | Microservice nhúng vector mô hình `microsoft/harrier-oss-v1-0.6b` |
| **PostgreSQL + PostGIS**| `5432` | `5432` | CSDL quan hệ lưu Users, tọa độ không gian sạt lở, rủi ro |

> [!TIP]
> **Ưu điểm của thiết kế Nginx Proxy nội bộ trên Port 3000:**
> Người dùng và các thiết bị bên ngoài **chỉ cần mở duy nhất Port 3000**. Trình duyệt gọi `/api/v1/...` sẽ được Nginx tại port 3000 chuyển tiếp trực tiếp vào `backend:8000` bên trong Docker network `terraalert-network`. Bạn **không cần** phải mở port 8000 ra internet, giúp tăng cường tối đa tính bảo mật và triệt tiêu hoàn toàn lỗi CORS.
> *(Lưu ý: Nếu port 3000 trên máy chủ của bạn bị trùng với dịch vụ khác, bạn có thể dễ dàng đổi port bằng biến môi trường `FRONTEND_PORT=3001` mà không cần sửa code).*

---

## 2. Cách 1: Chạy Trên Server Bằng Docker (Khuyến Nghị - Port 3000)

### 2.1. Yêu cầu hệ thống (Prerequisites)
- Hệ điều hành: Ubuntu 20.04 / 22.04 / 24.04 LTS, Debian, CentOS, AlmaLinux, Rocky Linux hoặc bất kỳ bản phân phối Linux nào.
- Phần cứng tối thiểu: 2 vCPU, 4GB RAM (Khuyến nghị 4 vCPU, 8GB RAM để chạy mượt mà Harrier 0.6B và Reranker).
- Cài đặt sẵn Docker & Docker Compose:
  ```bash
  # Kiểm tra cài đặt Docker
  docker --version
  docker compose version
  ```

### 2.2. Chuẩn bị biến môi trường (Environment Variables)
Sao chép file cấu hình mẫu và điền API Key của bạn:
```bash
cp backend/.env.example backend/.env
```
Mở file `backend/.env` để kiểm tra hoặc điền `GEMINI_API_KEY`:
```bash
nano backend/.env
```
*Nội dung mẫu cấu hình sẵn sàng:*
```env
APP_NAME=TerraAlert API
APP_VERSION=0.1.0
DEBUG=false

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/terraalert
CHROMA_HOST=chromadb
CHROMA_PORT=8000

ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000","http://localhost:5173"]
EMBEDDING_SERVICE_URL=http://embedding_service:8002/embed

GEMINI_API_KEY=AIzaSy... (API Key của bạn)
SECRET_KEY=terrasecret12345_production_change_me
```

### 2.3. Khởi chạy toàn bộ hệ thống (One-command Start)
Tại thư mục gốc dự án:
```bash
# Build và chạy ngầm toàn bộ 5 containers (Port 3000)
docker compose up -d --build
```

Kiểm tra trạng thái các container đang chạy:
```bash
docker compose ps
```
*Kết quả hiển thị trạng thái `Up` cho:*
- `rag-natural-disaster-frontend-1` -> `0.0.0.0:3000->80/tcp`
- `rag-natural-disaster-backend-1` -> `0.0.0.0:8000->8000/tcp`
- `rag-natural-disaster-chromadb-1` -> `0.0.0.0:8001->8000/tcp`
- `rag-natural-disaster-embedding_service-1` -> `0.0.0.0:8002->8002/tcp`
- `rag-natural-disaster-postgres-1` -> `0.0.0.0:5432->5432/tcp`

### 2.4. Nạp dữ liệu 7 tài liệu thiên tai miền núi vào hệ thống (Seeding)
Sau khi các dịch vụ đã khởi động, chạy lệnh sau để tự động phân đoạn (chunking) và nạp 7 tài liệu PCTT từ `filtered_pdf_markdown/` vào ChromaDB:
```bash
docker compose exec backend python scripts/seed_knowledge_base.py
```

### 2.5. Kiểm tra truy cập
- **Giao diện người dùng Web**: Truy cập `http://<IP_SERVER_CUA_BAN>:3000`
- **Tài liệu API (Swagger UI)**: Truy cập `http://<IP_SERVER_CUA_BAN>:8000/docs` (hoặc qua proxy: `http://<IP_SERVER_CUA_BAN>:3000/api/v1/...`)
- **Tài khoản quản trị mặc định**:
  - Email: `admin@terraalert.com`
  - Password: `admin`

---

## 3. Hướng Dẫn Mở Cổng 3000 Trên Server (Firewall & Cloud Security Groups)

Nếu bạn đã chạy Docker nhưng từ máy tính cá nhân không mở được `http://<IP_SERVER>:3000`, nguyên nhân 99% là do tường lửa đang chặn cổng 3000. Hãy thực hiện theo hướng dẫn tương ứng với môi trường máy chủ của bạn:

### 3.1. Đối với máy chủ Ubuntu / Debian (Sử dụng UFW)
UFW (Uncomplicated Firewall) là công cụ tường lửa phổ biến nhất trên Ubuntu:

1. **Kiểm tra trạng thái tường lửa hiện tại:**
   ```bash
   sudo ufw status
   ```
2. **Mở cổng 3000 cho giao thức TCP:**
   ```bash
   sudo ufw allow 3000/tcp comment 'TERRA Web App Frontend'
   ```
3. *(Tùy chọn) Mở thêm cổng 80, 443 nếu dùng Nginx ngoài:*
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```
4. **Tải lại tường lửa để áp dụng thay đổi:**
   ```bash
   sudo ufw reload
   ```
5. **Kiểm tra lại danh sách cổng đã mở:**
   ```bash
   sudo ufw status numbered
   ```
   *Bạn sẽ thấy dòng `3000/tcp ALLOW IN Anywhere`.*

---

### 3.2. Đối với máy chủ CentOS / RHEL / AlmaLinux / Rocky Linux (Sử dụng Firewalld)
1. **Mở cổng 3000 vĩnh viễn:**
   ```bash
   sudo firewall-cmd --permanent --zone=public --add-port=3000/tcp
   ```
2. **Tải lại cấu hình:**
   ```bash
   sudo firewall-cmd --reload
   ```
3. **Xác nhận cổng đã mở:**
   ```bash
   sudo firewall-cmd --list-ports
   ```

---

### 3.3. Đối với hệ thống dùng trực tiếp Iptables
1. **Thêm quy tắc cho phép TCP cổng 3000:**
   ```bash
   sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT
   ```
2. **Lưu lại quy tắc để không bị mất khi reboot:**
   ```bash
   # Trên Ubuntu/Debian:
   sudo apt-get install -y iptables-persistent
   sudo netfilter-persistent save
   
   # Hoặc:
   sudo iptables-save | sudo tee /etc/iptables/rules.v4
   ```

---

### 3.4. Cấu hình trên các nền tảng Cloud (Cloud Security Groups / Firewalls)

Nếu thuê VPS/Cloud, bạn cần mở cổng ở **Bảng điều khiển Web (Cloud Dashboard)** ngoài việc mở trên máy chủ:

#### A. Amazon Web Services (AWS EC2)
1. Đăng nhập AWS Management Console -> Dịch vụ **EC2** -> **Instances**.
2. Chọn máy ảo của bạn -> Nhấp vào tab **Security**.
3. Bấm vào tên **Security Group**.
4. Chọn tab **Inbound rules** -> Bấm **Edit inbound rules**.
5. Bấm **Add rule**:
   - **Type**: `Custom TCP`
   - **Port range**: `3000`
   - **Source**: `0.0.0.0/0` (Truy cập công khai) hoặc điền IP văn phòng/cá nhân của bạn.
   - **Description**: `TERRA Frontend Web App`
6. Bấm **Save rules**.

#### B. Google Cloud Platform (GCP Compute Engine)
1. Đăng nhập Google Cloud Console -> **VPC network** -> **Firewall**.
2. Nhấp vào **Create Firewall Rule**:
   - **Name**: `allow-terra-frontend-3000`
   - **Targets**: `All instances in the network` (hoặc chỉ định target tag).
   - **Source IPv4 ranges**: `0.0.0.0/0`
   - **Protocols and ports**: Tích chọn `Specified protocols and ports` -> Tích `TCP` -> Điền `3000`.
3. Bấm **Create**.

*Hoặc chạy nhanh 1 câu lệnh qua Google Cloud Shell:*
```bash
gcloud compute firewall-rules create allow-port-3000 \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:3000 \
    --source-ranges=0.0.0.0/0 \
    --description="Allow inbound traffic on port 3000 for TERRA Frontend"
```

#### C. DigitalOcean / Linode / Vultr / Hetzner
1. Vào mục **Networking** / **Firewalls**.
2. Tìm Firewall đang gắn với VPS/Droplet của bạn.
3. Thêm **Inbound Rule**:
   - **Protocol**: `TCP`
   - **Port**: `3000`
   - **Sources**: `All IPv4` (`0.0.0.0/0`) và `All IPv6` (`::/0`).
4. Bấm **Save Rule**.

#### D. Các nhà cung cấp Cloud tại Việt Nam (Viettel IDC, VNPT Cloud, FPT Smart Cloud, Bizfly, CMC)
1. Vào trang Quản lý máy chủ ảo / Virtual Machines.
2. Chọn mục **Security Group** hoặc **Firewall / Network Rules**.
3. Thêm Luật cho phép đến (Inbound): Giao thức `TCP`, Cổng `3000`, Dải IP nguồn `0.0.0.0/0`.
4. Áp dụng (Apply) vào VM.

---

### 3.5. Kiểm tra kiểm chứng xem Port 3000 đã lắng nghe & thông suốt chưa
1. **Kiểm tra trên máy chủ xem Docker đã lắng nghe port 3000 chưa:**
   ```bash
   sudo ss -tulpn | grep 3000
   # hoặc:
   sudo netstat -tlpn | grep 3000
   ```
   *Cần thấy tiến trình `docker-proxy` đang LISTEN trên `0.0.0.0:3000`.*

2. **Kiểm tra từ máy tính cá nhân qua cURL hoặc Telnet/Nmap:**
   ```bash
   curl -I http://<IP_SERVER_CUA_BAN>:3000
   ```
   *Nếu trả về `HTTP/1.1 200 OK` nghĩa là port đã thông hoàn toàn!*

---

## 4. Cách 2: Chạy Môi Trường Cục Bộ Cho Lập Trình Viên (Local Development)

Nếu bạn muốn debug trực tiếp mã nguồn Frontend React và Backend Python mà không thông qua Docker:

### 4.1. Khởi động các dịch vụ phụ trợ (PostgreSQL, ChromaDB, Embedding)
Bạn có thể dùng Docker Compose chỉ để chạy các dịch vụ database và embedding:
```bash
docker compose up -d postgres chromadb embedding_service
```

### 4.2. Chạy Backend (Python FastAPI)
1. Tạo và kích hoạt môi trường ảo:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Khởi chạy server FastAPI:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 4.3. Chạy Frontend (Vite Dev Server)
1. Cài đặt dependencies và chạy dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Giao diện dev sẽ mở tại: `http://localhost:5173`.
   *Vite đã được cấu hình proxy tự động chuyển tiếp `/api` về `http://localhost:8000`, đồng thời `config/api.ts` tự động phát hiện chế độ dev.*

---

## 5. Cấu Hình Tùy Chọn: Tên Miền & Chứng Chỉ SSL HTTPS (Nginx Reverse Proxy)

Để đưa hệ thống vào vận hành chính thức với tên miền (ví dụ: `https://thientai.domain.com`), bạn có thể cấu hình Nginx bên ngoài máy chủ trỏ về Port 3000:

1. **Tạo file cấu hình Nginx:**
   ```nginx
   server {
       listen 80;
       server_name thientai.domain.com;

       location / {
           proxy_pass http://127.0.0.1:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
2. **Cài đặt chứng chỉ SSL miễn phí qua Let's Encrypt (Certbot):**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d thientai.domain.com
   ```
   *Certbot sẽ tự động cấu hình HTTPS chuyển hướng và gia hạn SSL trọn đời.*

---

## 6. Các Lệnh Quản Trị Hữu Ích (Cheat Sheet)

```bash
# Xem log thời gian thực của toàn bộ hệ thống
docker compose logs -f

# Xem riêng log của backend
docker compose logs -f backend

# Xem riêng log của frontend
docker compose logs -f frontend

# Khởi động lại toàn bộ dịch vụ
docker compose restart

# Dừng hệ thống
docker compose down

# Dừng và xóa toàn bộ dữ liệu volume (thận trọng!)
docker compose down -v
```
