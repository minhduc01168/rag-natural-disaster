# 🏗️ TerraAlert — Tài Liệu Kiến Trúc Hệ Thống
> **Phiên bản:** 1.0 · **Ngày:** 2026-06-06 · **Tác giả:** Nguyễn Minh Đức

---

## 1. Tổng Quan Kiến Trúc

**TerraAlert** áp dụng kiến trúc **Dual-Lane** (Phân tách Thời gian – Không gian) theo nguyên tắc **CQRS** để giải quyết mâu thuẫn cốt lõi: xử lý cứu nạn tức thời (< 1s) song song với suy luận AI/ML phức tạp (5–10s).

| Thuộc tính | Giá trị |
|---|---|
| **Kiến trúc** | Dual-Lane + CQRS + Event-Driven |
| **Runtime** | Python 3.9+, Node.js 18+ |
| **Containerization** | Docker + Docker Compose |
| **Database** | PostgreSQL 15 + PostGIS / ChromaDB / Redis |
| **AI Framework** | LangChain · LlamaIndex · Gemini / Groq |
| **ML** | scikit-learn Random Forest · XGBoost |

---

## 2. Sơ Đồ Kiến Trúc Tổng Thể (System Architecture Overview)

```mermaid
graph TB
    %% ─────────────── USER LAYER ───────────────
    subgraph USER["👤 Người dùng cuối"]
        U1["🏠 Người dân vùng núi"]
        U2["🚨 Cán bộ cứu hộ"]
        U3["🔬 Nhà nghiên cứu"]
    end

    %% ─────────────── CLIENT LAYER ───────────────
    subgraph FE["📱 PWA Frontend · React 18 + TypeScript + Vite"]
        direction LR
        P1["🏠 Home &<br/>Emergency Dashboard"]
        P2["🚨 Alert Center<br/>(Cảnh báo màu)"]
        P3["📖 Offline Survival<br/>Guide (IndexedDB)"]
        P4["🗺️ Research Dashboard<br/>(Leaflet / GIS)"]
        P5["🤖 TerraBot Space<br/>(Chatbot UI)"]
    end

    %% ─────────────── GATEWAY LAYER ───────────────
    GW["🔀 API Gateway / Nginx\n:80 → :8000 reverse proxy\nCORS · Rate Limit · TLS"]

    %% ─────────────── FAST LANE ───────────────
    subgraph FL["⚡ FAST LANE — Độ trễ < 1 giây"]
        direction TB
        FA["FastAPI Core\n:8000/api/v1/fast-lane"]
        WS["WebSocket Server\n/ws/alerts"]
        AE["Alert Engine\n(Rule-based Classifier)\nXanh / Vàng / Đỏ"]
        NS["Notification Service\nConnectionManager"]
        WP["Weather Service\nMeteostat API"]
        SOS_H["SOS Handler\nPOST /sos"]
    end

    %% ─────────────── SLOW LANE ───────────────
    subgraph SL["🧠 SLOW LANE — AI · ML · GIS (5–10 giây)"]
        direction TB
        RA["FastAPI RAG Service\n:8000/api/v1/slow-lane"]

        subgraph AGENTS["🤖 Multi-Agent RAG System (LangChain)"]
            direction LR
            SA["SynthesisAgent\n(Router & Orchestrator)"]
            WA["WeatherAgent\n(Phân tích khí tượng)"]
            GA["GeoAgent\n(Phân tích địa hình)"]
            KA["KnowledgeAgent\n(Tra cứu tài liệu)"]
        end

        subgraph ML["📊 ML Pipeline"]
            TR["LSM Trainer\nRandom Forest · XGBoost"]
            PKL["model.pkl\n(Trained Model)"]
        end

        subgraph TASKS["⚙️ Celery Workers"]
            C1["Data Ingestion Task\n(Lấy dữ liệu vệ tinh)"]
            C2["ML Training Task\n(Huấn luyện batch)"]
        end
    end

    %% ─────────────── DATA LAYER ───────────────
    subgraph DATA["🗄️ Data Layer"]
        PG[("PostgreSQL 15\n+ PostGIS\n:5432")]
        RD[("Redis 7\nBroker · Cache\n:6379")]
        CH[("ChromaDB\nVector DB\n:8001")]
    end

    %% ─────────────── EXTERNAL APIs ───────────────
    subgraph EXT["🌐 External Data Sources"]
        MET["☁️ Meteostat API\n(Thời tiết thực)"]
        GEE["🛰️ Google Earth Engine\nSRTM · Sentinel-2 · GPM"]
        HDX["📊 HDX / DesInventar\n(Dữ liệu sạt lở lịch sử)"]
        LLM_API["🧠 LLM API\nGemini Flash · Groq"]
    end

    %% ─────────────── CONNECTIONS ───────────────
    USER --> FE
    FE -->|"HTTPS REST / WebSocket"| GW
    GW -->|"SOS, Weather, Alerts"| FA
    GW -->|"Chat, GIS, ML"| RA

    FA --> WS & AE & SOS_H & WP
    WP -->|"GET weather"| MET
    AE --> NS
    NS --> WS

    RA --> AGENTS
    SA --> WA & GA & KA
    WA -->|"fetch weather context"| WP
    GA -->|"query spatial data"| PG
    KA -->|"vector search"| CH
    KA -->|"generate response"| LLM_API

    TR --> PKL
    PKL -->|"generate LSM GeoJSON"| PG

    TASKS <-->|"task queue"| RD
    C1 -->|"pull satellite data"| GEE
    C1 -->|"pull disaster history"| HDX
    C1 -->|"store GIS data"| PG
    C2 --> TR

    RA -->|"read LSM / GIS"| PG
    RA -->|"embed docs"| CH

    %% Styles
    classDef lane fill:#1a1a2e,color:#e0e0ff,stroke:#4f46e5,stroke-width:2px
    classDef fastNode fill:#7f1d1d,color:#fecaca,stroke:#dc2626,stroke-width:1.5px
    classDef slowNode fill:#14532d,color:#bbf7d0,stroke:#16a34a,stroke-width:1.5px
    classDef dbNode fill:#1e3a5f,color:#bfdbfe,stroke:#3b82f6,stroke-width:1.5px
    classDef extNode fill:#3b1f5e,color:#e9d5ff,stroke:#9333ea,stroke-width:1.5px
    classDef feNode fill:#1c3028,color:#a7f3d0,stroke:#10b981,stroke-width:1.5px
    classDef gwNode fill:#292524,color:#fde68a,stroke:#f59e0b,stroke-width:2px

    class FL lane
    class SL lane
    class FA,WS,AE,NS,WP,SOS_H fastNode
    class RA,SA,WA,GA,KA,TR,PKL,C1,C2 slowNode
    class PG,RD,CH dbNode
    class MET,GEE,HDX,LLM_API extNode
    class P1,P2,P3,P4,P5 feNode
    class GW gwNode
```

---

## 3. Sơ Đồ Luồng Dữ Liệu — Fast Lane (Real-time Emergency)

```mermaid
sequenceDiagram
    actor User as 👤 Người dùng
    participant FE as 📱 PWA Frontend
    participant GW as 🔀 Nginx Gateway
    participant FA as ⚡ FastAPI Core
    participant WP as ☁️ Meteostat API
    participant AE as 🔴 Alert Engine
    participant WS as 📡 WebSocket
    participant NS as 🔔 Notification Svc

    %% ── SOS Flow ──
    rect rgb(127, 29, 29)
        note right of User: 🆘 Luồng SOS (< 1s)
        User ->> FE: Nhấn nút SOS
        FE ->> GW: POST /api/v1/fast-lane/sos<br/>{lat, lon, phone, message}
        GW ->> FA: forward request
        FA -->> FE: {status: "received", ticket_id: "SOS-xxx"}
        FE -->> User: "✅ Tín hiệu SOS đã gửi"
    end

    %% ── Weather Alert Flow ──
    rect rgb(78, 63, 0)
        note right of FA: ⏱️ Polling 3 giờ/lần (Cronjob)
        FA ->> WP: GET /weather/{lat}/{lon}
        WP -->> FA: {temp, humidity, wind_speed, rainfall}
        FA ->> AE: classify_weather(params)
        AE -->> FA: AlertLevel {GREEN/YELLOW/RED}
        alt Alert Level = RED hoặc YELLOW
            FA ->> NS: broadcast_alert(level, message)
            NS ->> WS: push to all connections
            WS -->> FE: {type: "alert", level: "RED", ...}
            FE -->> User: 🔴 Push Notification
        end
    end

    %% ── WebSocket Handshake ──
    rect rgb(20, 50, 80)
        note right of User: 🔌 WebSocket Connection
        User ->> FE: Mở App
        FE ->> GW: WS /api/v1/fast-lane/ws/alerts
        GW ->> FA: upgrade to WebSocket
        FA ->> NS: connect(websocket)
        loop Keep-alive
            FE -->> FA: ping
            FA -->> FE: pong
        end
    end
```

---

## 4. Sơ Đồ Luồng Dữ Liệu — Slow Lane (AI / RAG)

```mermaid
sequenceDiagram
    actor User as 👤 Người dùng
    participant FE as 📱 TerraBot UI
    participant GW as 🔀 Nginx
    participant RA as 🧠 RAG FastAPI
    participant SA as 🎯 SynthesisAgent
    participant WA as 🌦️ WeatherAgent
    participant GA as 🗺️ GeoAgent
    participant KA as 📚 KnowledgeAgent
    participant CH as 🗄️ ChromaDB
    participant PG as 🗄️ PostGIS
    participant LLM as 🤖 Gemini/Groq

    User ->> FE: "Bão sắp đến, nhà ở sườn đồi<br/>cần gia cố thế nào?"
    FE ->> GW: POST /api/v1/slow-lane/chat<br/>{message, context}
    GW ->> RA: forward

    RA ->> SA: process(query, context)
    
    note over SA: 🔍 Confidence-based Routing
    SA ->> WA: can_handle(query) → 0.6
    SA ->> GA: can_handle(query) → 0.7
    SA ->> KA: can_handle(query) → 0.8 ✅ WINNER

    SA ->> KA: process(query, context)
    
    KA ->> CH: similarity_search("gia cố nhà sườn đồi")
    CH -->> KA: [chunk1, chunk2, chunk3] (Top-K docs)
    
    KA ->> LLM: generate(prompt + chunks + query)
    LLM -->> KA: "Để gia cố nhà ở sườn đồi khi có bão..."

    KA -->> SA: {response, sources, confidence}
    SA -->> RA: format_response(...)
    RA -->> GW: {response, sources, agent}
    GW -->> FE: JSON response
    FE -->> User: 💬 Câu trả lời + nguồn tham khảo
```

---

## 5. Sơ Đồ Celery Worker — Data Ingestion Pipeline

```mermaid
graph LR
    subgraph SCHED["⏰ Scheduler (Celery Beat)"]
        CR1["Cron: mỗi 3h\ningest_weather_task"]
        CR2["Cron: hàng ngày\nupdate_gis_task"]
        CR3["Manual Trigger\ntrain_ml_task"]
    end

    subgraph BROKER["📨 Redis Broker :6379"]
        Q1["Queue: fast-queue"]
        Q2["Queue: slow-queue"]
    end

    subgraph WORKERS["⚙️ Celery Workers"]
        W1["Worker 1\nData Ingestion"]
        W2["Worker 2\nML Training"]
    end

    subgraph EXT_DATA["🌐 External Sources"]
        GEE2["🛰️ Google Earth Engine\nSRTM DEM 30m\nSentinel-2 NDVI\nNASA GPM IMERG"]
        HDX2["📊 HDX OCHA\nDesInventar Sendai\nSạt lở lịch sử VN"]
        MET2["☁️ Meteostat\nStation data"]
    end

    subgraph STORAGE["🗄️ Storage"]
        PG2[("PostgreSQL + PostGIS\nBảng: gis_layers\nBảng: disaster_events\nBảng: weather_snapshots")]
        PKL2["model.pkl\n(Trained Random Forest)"]
    end

    CR1 --> Q1
    CR2 --> Q2
    CR3 --> Q2

    Q1 --> W1
    Q2 --> W1 & W2

    W1 -->|"ee.Image().getInfo()"| GEE2
    W1 -->|"download CSV/Shapefile"| HDX2
    W1 -->|"stations API"| MET2
    W1 -->|"INSERT GIS data"| PG2

    W2 -->|"SELECT features"| PG2
    W2 -->|"train RF model"| PKL2
    PKL2 -->|"generate_lsm_grid()"| PG2
```

---

## 6. Sơ Đồ Multi-Agent RAG — Chi Tiết

```mermaid
graph TD
    subgraph ROUTER["🎯 SynthesisAgent (Orchestrator)"]
        SA2["SynthesisAgent\ncan_handle → 0.5 (default)"]
        ROUTE{"Confidence\nRouting\nmax(scores)"}
    end

    subgraph SPEC_AGENTS["🤖 Specialized Agents"]
        WA2["🌦️ WeatherAgent\nKeywords: thời tiết, mưa,\nbão, nhiệt độ, độ ẩm\nConfidence: 0.0 – 1.0"]
        GA2["🗺️ GeoAgent\nKeywords: vị trí, địa hình,\nsườn đồi, tọa độ, bản đồ\nConfidence: 0.0 – 1.0"]
        KA2["📚 KnowledgeAgent\nDefault fallback\nRAG over ChromaDB\nConfidence: 0.0 – 1.0"]
    end

    subgraph RAG_STACK["📖 RAG Stack"]
        EMBED["Embedding Model\n(text-embedding-*)"]
        VDB["ChromaDB\nVector Store\nCollection: disaster_docs"]
        TOPK["Top-K Retrieval\nSimilarity Search"]
        PROMPT["Prompt Template\n(system + context + query)"]
        LLM2["LLM API\nGemini Flash / Groq\nLlama-3 / Mixtral"]
    end

    subgraph KB["📂 Knowledge Base"]
        DOC1["📄 Tài liệu phòng chống thiên tai"]
        DOC2["📄 Hướng dẫn sơ tán"]
        DOC3["📄 Kỹ năng sinh tồn"]
    end

    USER_Q["💬 User Query"] --> SA2
    SA2 --> ROUTE
    ROUTE -->|"score < 0.3 → default"| KA2
    ROUTE -->|"weather keywords"| WA2
    ROUTE -->|"geo keywords"| GA2

    DOC1 & DOC2 & DOC3 -->|"chunk + embed"| EMBED
    EMBED -->|"upsert vectors"| VDB

    KA2 --> VDB
    VDB --> TOPK
    TOPK --> PROMPT
    WA2 -->|"inject weather data"| PROMPT
    GA2 -->|"inject PostGIS data"| PROMPT
    PROMPT --> LLM2
    LLM2 -->|"response + sources"| SA2
    SA2 -->|"_format_response()"| RESP["📤 {response, sources, confidence}"]
```

---

## 7. Sơ Đồ Triển Khai Docker (Deployment Diagram)

```mermaid
graph TB
    subgraph HOST["🖥️ Docker Host (Local / VPS)"]
        subgraph NET["Docker Network: terraalert-network (bridge)"]
            subgraph FE_C["Container: frontend · :3000→:80"]
                NGINX_FE["Nginx\nServe React PWA\n+ Service Worker"]
            end

            subgraph BE_C["Container: backend · :8000→:8000"]
                UVICORN["Uvicorn ASGI\nFastAPI App\n/api/v1/fast-lane\n/api/v1/slow-lane\n/health · /docs"]
            end

            subgraph PG_C["Container: postgres · :5432→:5432"]
                PG_DB[("PostgreSQL 15 Alpine\nDB: terraalert\nExtension: PostGIS")]
            end

            subgraph RD_C["Container: redis · :6379→:6379"]
                RD_SVC[("Redis 7 Alpine\nBroker + Cache")]
            end

            subgraph CH_C["Container: chromadb · :8001→:8000"]
                CH_SVC[("ChromaDB latest\nPersistent Vector Store")]
            end
        end

        subgraph VOLS["📦 Docker Volumes"]
            V1["postgres_data"]
            V2["redis_data"]
            V3["chroma_data"]
        end
    end

    subgraph BROWSER["🌐 Browser / Mobile"]
        PWA["PWA Client\nService Worker\nIndexedDB (Offline)"]
    end

    PWA -->|":3000"| FE_C
    FE_C -->|":8000 API"| BE_C
    BE_C -->|":5432"| PG_C
    BE_C -->|":6379"| RD_C
    BE_C -->|":8001"| CH_C

    PG_C --- V1
    RD_C --- V2
    CH_C --- V3
```

---

## 8. Sơ Đồ Cơ Sở Dữ Liệu (ER Diagram)

```mermaid
erDiagram
    DISASTER_EVENTS {
        int id PK
        varchar event_type "landslide / flood / storm"
        geometry location "PostGIS Point SRID-4326"
        date event_date
        varchar source "HDX / DesInventar"
        float severity_score
        text description
        jsonb metadata
        timestamp created_at
    }

    GIS_LAYERS {
        int id PK
        varchar layer_name "elevation / ndvi / rainfall"
        geometry bounds "PostGIS Polygon"
        jsonb data "GeoJSON FeatureCollection"
        varchar source "SRTM / Sentinel-2 / GPM"
        float resolution_m "30m / 10m"
        timestamp fetched_at
    }

    WEATHER_SNAPSHOTS {
        int id PK
        float latitude
        float longitude
        float temperature "Celsius"
        float humidity "percent"
        float wind_speed "km per h"
        float rainfall "mm per h"
        varchar alert_level "GREEN / YELLOW / RED"
        timestamp recorded_at
    }

    SOS_SIGNALS {
        int id PK
        varchar ticket_id UK "SOS-YYYY-NNN"
        float latitude
        float longitude
        varchar phone
        text message
        varchar status "received / dispatched / resolved"
        timestamp created_at
    }

    LSM_RESULTS {
        int id PK
        geometry grid_cell "PostGIS Polygon"
        float susceptibility_score "0.0 to 1.0"
        varchar risk_level "LOW / MEDIUM / HIGH / VERY_HIGH"
        varchar model_version
        timestamp generated_at
    }

    GIS_LAYERS ||--o{ LSM_RESULTS : "used_to_generate"
    DISASTER_EVENTS }o--|| GIS_LAYERS : "co-located_with"
    WEATHER_SNAPSHOTS }o--o{ DISASTER_EVENTS : "correlated_with"
```

---

## 9. Sơ Đồ ML Pipeline (Landslide Susceptibility Model)

```mermaid
flowchart TD
    subgraph INGEST["📥 Data Ingestion (Celery Task — Daily)"]
        I1["🛰️ GEE: SRTM DEM\nslope, elevation, aspect"]
        I2["🛰️ GEE: Sentinel-2\nNDVI = NIR-Red / NIR+Red"]
        I3["🛰️ GEE: NASA GPM IMERG\nrainfall accumulation (mm)"]
        I4["📊 HDX: DesInventar\nLandslide occurrence points"]
    end

    subgraph PREP["⚙️ Feature Engineering (PostGIS)"]
        FE2["Spatial Join ST_Contains"]
        FEAT["Feature Matrix X\nslope, elevation, aspect,\nndvi, rainfall_7d, rainfall_30d"]
        LABEL["Label Vector y\n1=landslide · 0=no-event"]
    end

    subgraph TRAIN["🧠 Model Training (Kaggle / Local)"]
        SPLIT["Train / Test Split 80-20"]
        RF["Random Forest\nn_estimators=200\nmax_depth=15"]
        XGB["XGBoost\nBooster=gbtree"]
        EVAL["Evaluation\nAUC-ROC · Precision · Recall · F1"]
        EXPORT["Export model.pkl via joblib.dump"]
    end

    subgraph SERVE["🗺️ Model Serving (FastAPI)"]
        LOAD["joblib.load model.pkl\nLSMTrainer.load_model()"]
        GRID["generate_lsm_grid bounds resolution\nPredict on spatial grid"]
        GEOJSON["GeoJSON Output\nFeatureCollection\nsusceptibility_score · risk_level"]
        PGSTORE["Store to PostGIS\ntable: lsm_results"]
    end

    subgraph DISPLAY["📱 Frontend (Leaflet)"]
        LEAFLET["Choropleth Map\nColor gradient Green to Red"]
    end

    I1 & I2 & I3 --> FE2
    I4 --> FE2
    FE2 --> FEAT & LABEL
    FEAT & LABEL --> SPLIT
    SPLIT --> RF & XGB
    RF & XGB --> EVAL
    EVAL --> EXPORT

    EXPORT --> LOAD
    LOAD --> GRID
    GRID --> GEOJSON
    GEOJSON --> PGSTORE
    PGSTORE -->|"GET /slow-lane/map/susceptibility"| LEAFLET
```

---

## 10. Cấu Trúc Thư Mục Dự Án

```
rag-natural-disaster/
├── frontend/                       # React 18 + TypeScript + Vite PWA
│   ├── src/
│   │   ├── components/
│   │   │   ├── map/                # Leaflet map components
│   │   │   ├── chat/               # TerraBot chatbot UI
│   │   │   └── charts/             # Recharts / D3 visualizations
│   │   ├── pages/                  # 5 route pages
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── services/               # Axios API clients
│   │   └── data/                   # Static survival guide data
│   ├── public/                     # PWA assets, icons, manifest.json
│   ├── nginx.conf                  # Production web server config
│   └── Dockerfile                  # Multi-stage build: node → nginx
│
├── backend/                        # FastAPI + Python 3.9+
│   ├── app/
│   │   ├── main.py                 # FastAPI app factory + CORS
│   │   ├── api/router.py           # Aggregate routers
│   │   ├── core/config.py          # Pydantic Settings
│   │   ├── fast_lane/              # ⚡ Fast Lane (< 1s)
│   │   │   ├── router.py           # SOS · Weather · WebSocket
│   │   │   ├── services/
│   │   │   │   ├── weather_service.py      # Meteostat API client
│   │   │   │   ├── alert_engine.py         # Rule-based classifier
│   │   │   │   └── notification_service.py # WebSocket ConnectionManager
│   │   │   └── models/alert.py     # AlertLevel Pydantic model
│   │   └── slow_lane/              # 🧠 Slow Lane (5–10s)
│   │       ├── router.py           # Chat · LSM · GIS · Tasks
│   │       ├── agents/
│   │       │   ├── base_agent.py       # Abstract BaseAgent
│   │       │   ├── synthesis_agent.py  # Orchestrator (Router)
│   │       │   ├── weather_agent.py    # Weather context agent
│   │       │   ├── geo_agent.py        # Geographic context agent
│   │       │   └── knowledge_agent.py  # ChromaDB RAG agent
│   │       ├── ml/
│   │       │   ├── model_trainer.py    # LSMTrainer (RF + XGB)
│   │       │   └── models/             # Saved .pkl files
│   │       ├── knowledge/
│   │       │   └── document_loader.py  # PDF/Markdown chunker
│   │       ├── services/llm_service.py # Gemini/Groq API wrapper
│   │       ├── db/                     # PostGIS queries
│   │       └── tasks/                  # Celery tasks
│   ├── requirements.txt
│   └── Dockerfile
│
├── ml_training/                    # Offline Training Pipeline
│   ├── scripts/create_dataset.py   # GEE data extraction
│   └── *.ipynb                     # Kaggle training notebooks
│
├── docs/
│   ├── architecture.md             # 📖 This document
│   ├── system_requirements_document.md
│   └── epics_and_stories.md
│
└── docker-compose.yml              # 5 services orchestration
```

---

## 11. API Reference Summary

### Fast Lane (`/api/v1/fast-lane`)

| Method | Endpoint | Mô tả | SLA |
|--------|----------|-------|-----|
| `POST` | `/sos` | Gửi tín hiệu SOS (lat, lon, phone) | < 200ms |
| `GET` | `/weather/{lat}/{lon}` | Lấy thời tiết + mức cảnh báo | < 500ms |
| `GET` | `/alerts` | Danh sách cảnh báo hiện tại | < 100ms |
| `GET` | `/alert-level` | Phân loại cảnh báo từ weather params | < 50ms |
| `WS` | `/ws/alerts` | WebSocket realtime alerts | persistent |
| `GET` | `/ws/status` | Số WebSocket connections đang hoạt động | < 50ms |

### Slow Lane (`/api/v1/slow-lane`)

| Method | Endpoint | Mô tả | SLA |
|--------|----------|-------|-----|
| `POST` | `/chat` | Chat với TerraBot (multi-agent) | < 10s |
| `POST` | `/chat/stream` | Streaming chat response | < 5s TTFB |
| `GET` | `/map/susceptibility` | Bản đồ LSM GeoJSON | < 2s |
| `POST` | `/ml/generate-lsm` | Tạo LSM cho vùng cụ thể | < 30s |
| `POST` | `/ml/train` | Trigger huấn luyện model | async |
| `GET` | `/agents` | Danh sách agents khả dụng | < 50ms |
| `GET` | `/knowledge/categories` | Danh mục knowledge base | < 100ms |
| `GET` | `/data/gis` | Dữ liệu GIS tổng hợp | < 1s |
| `GET` | `/data/elevation` | Thông tin SRTM | < 50ms |
| `GET` | `/data/disasters` | Lịch sử thiên tai HDX | < 1s |
| `GET` | `/tasks/{task_id}` | Trạng thái Celery task | < 100ms |
| `GET` | `/worker/health` | Health check workers + Redis | < 50ms |

---

## 12. Non-Functional Requirements (SLAs)

| Chỉ số | Fast Lane | Slow Lane |
|--------|-----------|-----------|
| **Độ trễ P95** | < 1 giây | < 10 giây |
| **Throughput** | 100 req/s | 10 req/s |
| **Availability** | 99.9% | 99.0% |
| **Offline support** | ✅ PWA + Service Worker | ❌ Cần internet |
| **WebSocket** | ✅ Persistent realtime | ❌ N/A |
| **Streaming** | ❌ N/A | ✅ SSE / Server-Sent Events |

---

> 📌 **Ghi chú:** Tài liệu này được xây dựng từ phân tích source code thực tế ngày 2026-06-06.
> Cập nhật tài liệu này mỗi khi có thay đổi kiến trúc.
