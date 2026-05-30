# TerraAlert - Hệ thống Cảnh báo & Hỗ trợ Sạt lở Đất

<p align="center">
  <img src="frontend/public/icons/icon-192x192.svg" alt="TerraAlert Logo" width="120">
</p>

<p align="center">
  <strong>Hệ thống cảnh báo thiên tai thông minh ứng dụng AI/ML và RAG cho Việt Nam</strong>
</p>

<p align="center">
  <a href="#-tính-năng-chính">Tính năng</a> •
  <a href="#-công-nghệ">Công nghệ</a> •
  <a href="#-cài-đặt">Cài đặt</a> •
  <a href="#-cấu-trúc-dự-án">Cấu trúc</a> •
  <a href="#-api">API</a> •
  <a href="#-liên-hệ">Liên hệ</a>
</p>

---

## Tổng quan

**TerraAlert** là hệ thống cảnh báo và hỗ trợ ứng phó thiên tai sạt lở đất tại Việt Nam, được xây dựng với kiến trúc **dual-lane**:

- **Fast Lane** - Xử lý thời gian thực: Cảnh báo thời tiết, SOS, push notifications
- **Slow Lane** - Xử lý AI/ML: Phân tích GIS, huấn luyện mô hình dự đoán, chatbot RAG

### Bài toán giải quyết

Việt Nam nằm trong top 10 quốc gia chịu ảnh hưởng nặng nề nhất của biến đổi khí hậu, với hàng trăm vụ sạt lở đất mỗi năm. TerraAlert cung cấp:

1. **Cảnh báo sớm** dựa trên dữ liệu thời tiết realtime
2. **Bản đồ nhạy cảm sạt lở** (Landslide Susceptibility Map) bằng ML
3. **Chatbot AI** hỗ trợ tra cứu thông tin thiên tai
4. **Cẩm nang sinh tồn** hoạt động offline (PWA)

---

## Tính năng chính

### Fast Lane (Real-time)
- Dashboard cảnh báo khẩn cấp (Xanh/Vàng/Đỏ)
- Nút SOS gửi tín hiệu cứu hộ
- Thông báo push qua WebSockets
- Dữ liệu thời tiết realtime từ Meteostat API

### Slow Lane (AI/ML)
- Pipeline ingestion dữ liệu GIS (GEE, HDX, Meteostat)
- Huấn luyện mô hình Random Forest/XGBoost dự đoán sạt lở
- Multi-Agent RAG System (4 agents) với LangChain
- Chatbot TerraBot hỗ trợ tiếng Việt

### PWA (Progressive Web App)
- Hoạt động offline với Service Workers
- Cẩm nang sinh tồn số (IndexedDB)
- Responsive design cho mobile

### Research Dashboard
- Bản đồ GIS tương tác (Leaflet/Mapbox)
- Trực quan hóa LSM (Landslide Susceptibility Map)
- Biểu đồ time-series phân tích xu hướng

---

## Công nghệ

### Frontend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type safety |
| Vite | 5.x | Build tool |
| TailwindCSS | 3.x | Styling |
| React Router | 6.x | Routing |
| Leaflet | 1.9.x | Bản đồ |
| Zustand | 4.x | State management |

### Backend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| FastAPI | 0.109.x | Web framework |
| Python | 3.9+ | Runtime |
| Celery | 5.x | Task queue |
| PostgreSQL + PostGIS | 15+ | Database |
| Redis | 7.x | Cache/Queue |
| ChromaDB | 0.4.x | Vector DB |

### AI/ML
| Công nghệ | Mục đích |
|-----------|----------|
| scikit-learn | Random Forest, Gradient Boosting |
| XGBoost | Gradient Boosting model |
| LangChain | Multi-Agent RAG framework |
| LlamaIndex | Knowledge base |
| Google Gemini / Groq | LLM API |

### Infrastructure
| Công nghệ | Mục đích |
|-----------|----------|
| Docker | Containerization |
| Docker Compose | Orchestration |
| Nginx | Reverse proxy |

---

## Cài đặt

### Yêu cầu hệ thống

- Node.js >= 18.x
- Python >= 3.9
- Docker >= 24.x
- Docker Compose >= 2.x

### 1. Clone repository

```bash
git clone https://github.com/minhduc01168/rag-natural-disaster.git
cd rag-natural-disaster
```

### 2. Cài đặt với Docker Compose (Khuyến nghị)

```bash
docker compose up -d
```

Các services sẽ chạy tại:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- ChromaDB: localhost:8001

### 3. Cài đặt thủ công (Development)

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 4. Cấu hình Environment

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env với API keys của bạn

# Frontend
cp frontend/.env.example frontend/.env
```

Xem thêm: [INSTALLATION.md](INSTALLATION.md)

---

## Cấu trúc dự án

```
rag-natural-disaster/
├── frontend/                    # React PWA frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── map/             # Bản đồ (Leaflet)
│   │   │   ├── chat/            # Chatbot UI
│   │   │   └── charts/          # Biểu đồ
│   │   ├── pages/               # Pages
│   │   ├── hooks/               # Custom hooks
│   │   ├── services/            # API services
│   │   └── data/                # Static data
│   └── public/                  # PWA assets
│
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── fast_lane/           # Realtime processing
│   │   │   ├── models/          # Data models
│   │   │   └── services/        # Business logic
│   │   ├── slow_lane/           # AI/ML processing
│   │   │   ├── agents/          # RAG Agents
│   │   │   ├── ml/              # ML models
│   │   │   ├── knowledge/       # Knowledge base
│   │   │   ├── services/        # Data services
│   │   │   └── tasks/           # Celery tasks
│   │   ├── api/                 # API routers
│   │   └── core/                # Config, Celery
│   └── tests/                   # Unit tests
│
├── ml_training/                 # ML training notebooks
│   ├── scripts/                 # Data extraction scripts
│   └── *.ipynb                  # Jupyter notebooks
│
├── docs/                        # Documentation
├── docker-compose.yml           # Docker orchestration
└── README.md                    # This file
```

---

## API

### Fast Lane (Realtime)

| Method | Endpoint | Mô tả |
|--------|----------|--------|
| POST | `/api/v1/fast-lane/sos` | Gửi tín hiệu SOS |
| GET | `/api/v1/fast-lane/weather/{lat}/{lon}` | Lấy thời tiết |
| GET | `/api/v1/fast-lane/alerts` | Danh sách cảnh báo |

### Slow Lane (AI/ML)

| Method | Endpoint | Mô tả |
|--------|----------|--------|
| POST | `/api/v1/slow-lane/chat` | Chat với TerraBot |
| GET | `/api/v1/slow-lane/map/susceptibility` | Bản đồ LSM |
| GET | `/api/v1/slow-lane/data/gis` | Dữ liệu GIS |

### System

| Method | Endpoint | Mô tả |
|--------|----------|--------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc |

---

## ML Training

### Dataset

Dữ liệu huấn luyện được tạo từ các nguồn công cộng:

| Nguồn | Dữ liệu | Link |
|-------|----------|------|
| NASA GPM/CHIRPS | Lượng mưa | Google Earth Engine |
| SRTM DEM | Địa hình | Google Earth Engine |
| Sentinel-2 | NDVI | Google Earth Engine |
| HDX/DesInventar | Lịch sử sạt lở | data.humdata.org |

### Huấn luyện

Xem hướng dẫn chi tiết: [ml_training/DATASET_GUIDE.md](ml_training/DATASET_GUIDE.md)

```bash
# Tạo dataset từ GEE
python ml_training/scripts/create_dataset.py --output dataset.csv

# Upload lên Kaggle và chạy notebook
# ml_training/landslide_susceptibility_training.ipynb
```

---

## Roadmap

- [x] Project Setup & Foundation
- [ ] Fast Lane Core (Real-time SOS & Alerts)
- [ ] Offline Survival Guide (PWA)
- [ ] Slow Lane Data Ingestion & ML Pipeline
- [ ] Multi-Agent RAG System (TerraBot)
- [ ] Research Dashboard (GIS Visualization)

Xem chi tiết: [ROADMAP.md](ROADMAP.md)

---

## Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/ten-feature`)
3. Commit changes (`git commit -m 'feat: Add feature'`)
4. Push to branch (`git push origin feature/ten-feature`)
5. Tạo Pull Request

---

## License

Dự án được phát triển cho mục đích học thuật.

---

<p align="center">
  <em>TerraAlert - Bảo vệ cộng đồng trước thiên tai</em>
</p>
