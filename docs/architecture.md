# 🏗️ TerraAlert — Tài Liệu Kiến Trúc Hệ Thống (Advanced RAG)
> **Phiên bản:** 2.0 · **Ngày:** 2026-06-06 · **Tác giả:** Nguyễn Minh Đức

---

## 1. Tổng Quan Kiến Trúc

**TerraAlert** áp dụng kiến trúc **Dual-Lane** (Phân tách Thời gian – Không gian) theo nguyên tắc **CQRS** để giải quyết mâu thuẫn cốt lõi: xử lý cứu nạn tức thời (< 1s) song song với suy luận AI phức tạp (5–10s). Trong phiên bản 2.0, hệ thống tập trung hoàn toàn vào **Advanced Agentic RAG** để hỗ trợ ra quyết định thay vì dùng ML truyền thống.

| Thuộc tính | Giá trị |
|---|---|
| **Kiến trúc** | Dual-Lane + CQRS + Event-Driven |
| **Runtime** | Python 3.9+, Node.js 18+ |
| **Containerization** | Docker + Docker Compose |
| **Database** | PostgreSQL 15 + PostGIS / ChromaDB / Redis |
| **AI Framework** | LangChain · LlamaIndex · Gemini / Groq |
| **Advanced RAG** | Semantic Chunking · Hybrid Search · Cross-Encoder Reranking |

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
        P4["🤖 TerraBot Space<br/>(Chatbot UI)"]
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

    %% ─────────────── SLOW LANE (AGENTIC RAG) ───────────────
    subgraph SL["🧠 SLOW LANE — Advanced RAG (5–10 giây)"]
        direction TB
        RA["FastAPI RAG Service\n:8000/api/v1/slow-lane"]

        subgraph AGENTS["🤖 Multi-Agent System (LangChain)"]
            direction LR
            SA["SynthesisAgent\n(Router & Orchestrator)"]
            WA["WeatherAgent\n(API Thời tiết)"]
            GA["GeoAgent\n(API Địa hình)"]
            KA["KnowledgeAgent\n(Tra cứu RAG)"]
        end

        subgraph RAG_CORE["📚 Advanced RAG Core"]
            ING["Ingestion Engine\n(Semantic Chunking)"]
            RET["Retrieval Engine\n(Hybrid Search)"]
            RER["Reranker\n(Cross-Encoder)"]
        end

        subgraph TASKS["⚙️ Celery Workers"]
            C1["Document Ingestion Task\n(Parse PDF/Word)"]
            C2["Evaluation Task\n(RAGAS Benchmark)"]
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
        TOPO["🏔️ OpenTopoData\n(Độ cao/Độ dốc)"]
        LLM_API["🧠 LLM API\nGemini Flash · Groq"]
    end

    %% ─────────────── CONNECTIONS ───────────────
    USER --> FE
    FE -->|"HTTPS REST / WebSocket"| GW
    GW -->|"SOS, Weather, Alerts"| FA
    GW -->|"Chat, RAG"| RA

    FA --> WS & AE & SOS_H & WP
    WP -->|"GET weather"| MET
    AE --> NS
    NS --> WS

    RA --> AGENTS
    SA --> WA & GA & KA
    WA -->|"fetch weather"| WP
    GA -->|"fetch elevation"| TOPO
    
    KA --> RET
    RET -->|"query vectors"| CH
    RET --> RER
    RER -->|"generate response"| LLM_API

    TASKS <-->|"task queue"| RD
    C1 --> ING
    ING -->|"embed chunks"| CH
    C2 -->|"evaluate response"| LLM_API

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
    class RA,SA,WA,GA,KA,ING,RET,RER,C1,C2 slowNode
    class PG,RD,CH dbNode
    class MET,TOPO,LLM_API extNode
    class P1,P2,P3,P4 feNode
    class GW gwNode
```

---

## 3. Sơ Đồ Luồng Dữ Liệu — Fast Lane (Real-time Emergency)

*(Luồng Fast Lane được giữ nguyên, đảm bảo độ trễ < 1s cho SOS và Cảnh báo)*

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
        FE ->> GW: POST /api/v1/fast-lane/sos
        GW ->> FA: forward request
        FA -->> FE: {status: "received", ticket_id: "SOS-xxx"}
        FE -->> User: "✅ Tín hiệu SOS đã gửi"
    end
```

---

## 4. Sơ Đồ Luồng Dữ Liệu — Slow Lane (Advanced RAG)

```mermaid
sequenceDiagram
    actor User as 👤 Người dùng
    participant FE as 📱 TerraBot UI
    participant SA as 🎯 SynthesisAgent
    participant WA as 🌦️ WeatherAgent
    participant KA as 📚 KnowledgeAgent
    participant VDB as 🗄️ ChromaDB
    participant RER as 🔄 Cross-Encoder
    participant LLM as 🤖 LLM (Gemini)

    User ->> FE: "Trời đang mưa to, tôi ở sườn đồi cần sơ tán không?"
    FE ->> SA: process(query)
    
    note over SA: 🔍 Phân tích Ý định & Router
    SA ->> WA: Lấy thời tiết hiện tại
    WA -->> SA: "Mưa 50mm/h (Báo động Đỏ)"
    
    SA ->> KA: Lấy hướng dẫn sơ tán sạt lở
    KA ->> VDB: Hybrid Search (BM25 + Vector)
    VDB -->> KA: Top 10 chunks
    
    note over KA: 🔄 Reranking (Re-ranker)
    KA ->> RER: Xếp hạng lại 10 chunks
    RER -->> KA: Top 3 chunks chính xác nhất
    
    KA ->> LLM: Prompt (Context + Weather + Query)
    LLM -->> KA: Câu trả lời chi tiết
    
    KA -->> SA: Response + Nguồn tài liệu
    SA -->> FE: JSON Response
    FE -->> User: 💬 Câu trả lời + Quyết định sơ tán
```

---

## 5. Kiến Trúc Data Ingestion & Evaluation (Celery)

Thay vì huấn luyện ML, hệ thống tập trung vào việc xử lý tài liệu lớn và đánh giá RAG tự động.

```mermaid
graph LR
    subgraph KNOWLEDGE["📂 Knowledge Base"]
        PDF["Cẩm nang sơ cứu (PDF)"]
        DOC["Luật phòng chống thiên tai (Word)"]
    end

    subgraph INGESTION["⚙️ Celery Worker: Ingestion"]
        PARSE["Document Parser\n(Unstructured.io)"]
        CHUNK["Semantic Chunker\n(Tách theo ngữ nghĩa)"]
        EMBED["Embedding Model\n(text-embedding)"]
    end

    subgraph EVAL["⚙️ Celery Worker: Evaluation"]
        RAGAS["RAGAS Framework\n(Faithfulness, Context Precision)"]
    end

    PDF & DOC --> PARSE
    PARSE --> CHUNK
    CHUNK --> EMBED
    EMBED -->|"Upsert"| CH[("ChromaDB")]

    CH -.->|"Test Contexts"| RAGAS
```

---

## 6. Sơ Đồ Cơ Sở Dữ Liệu (ER Diagram)

```mermaid
erDiagram
    WEATHER_SNAPSHOTS {
        int id PK
        float latitude
        float longitude
        float temperature "Celsius"
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
        varchar status
        timestamp created_at
    }

    KNOWLEDGE_DOCS {
        int id PK
        varchar title
        varchar source_url
        varchar doc_type "pdf / word"
        timestamp ingested_at
    }
```

---

## 7. Cấu Trúc Thư Mục Backend Mới

```
backend/
├── app/
│   ├── main.py
│   ├── fast_lane/              # ⚡ Fast Lane (< 1s)
│   │   ├── router.py           # SOS · Weather · WebSocket
│   │   └── services/           # Alert Engine, Notifications
│   ├── api/
│   │   └── rag_router.py       # 🧠 Advanced RAG Endpoint
│   └── rag/                    # Lõi Advanced RAG
│       ├── agents/             # Synthesis, Weather, Geo, Knowledge, Router, LLMGenerator
│       ├── tools/              # API wrappers cho Tools
│       ├── ingestion/          # Semantic chunking, PDF parsing, VectorStore
│       ├── retrieval/          # Hybrid Search, Reranker
│       └── evaluation/         # RAGAS metrics & TruLens
├── tests/
│   ├── rag/                    # Unit tests & Mocking
│   └── test_main.py
└── docker-compose.yml
```
