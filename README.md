# TerraAlert - Hệ thống Cảnh báo & Hỗ trợ Sạt lở Đất (Agentic RAG)

<p align="center">
  <img src="frontend/public/icons/icon-192x192.svg" alt="TerraAlert Logo" width="120">
</p>

<p align="center">
  <strong>Hệ thống Agentic RAG thông minh cảnh báo và hỏi đáp thiên tai cho Việt Nam</strong>
</p>

<p align="center">
  <a href="#-tính-năng-chính">Tính năng</a> •
  <a href="#-công-nghệ">Công nghệ</a> •
  <a href="#-cài-đặt">Cài đặt</a> •
  <a href="#-cấu-trúc-dự-án">Cấu trúc</a> •
  <a href="#-api">API</a>
</p>

---

## Tổng quan

**TerraAlert** là hệ thống trợ lý ảo thông minh (TerraBot) chuyên sâu về cảnh báo và phòng chống thiên tai (đặc biệt là sạt lở đất) tại Việt Nam. Dự án đã được chuyển đổi (Pivot) sang kiến trúc **Agentic RAG (Retrieval-Augmented Generation)** để mang lại độ chính xác cao và khả năng tư duy linh hoạt.

### Bài toán giải quyết

Hàng năm Việt Nam đối mặt với hàng trăm vụ sạt lở đất. Việc tiếp cận thông tin cảnh báo và kiến thức phòng chống thường khô khan và thụ động. TerraBot giải quyết vấn đề này bằng cách:
1. Đóng vai trò chuyên gia phân tích dữ liệu thời tiết thực tế.
2. Tra cứu cẩm nang sinh tồn và kiến thức phòng chống thiên tai từ cơ sở dữ liệu Vector.
3. Tổng hợp và trả lời người dân một cách tự nhiên, thân thiện và chính xác.

---

## Tính năng chính

### 🤖 Multi-Agent Orchestration
Sử dụng kiến trúc Multi-Agent để xử lý các loại câu hỏi khác nhau:
- **Router Agent:** Phân loại ý định người dùng (Hỏi thời tiết hay Hỏi kiến thức).
- **Knowledge Agent:** Truy xuất cẩm nang thiên tai bằng Hybrid Search (ChromaDB + BM25) kết hợp Cross-Encoder Reranking.
- **Tools Agent:** Gọi API thời tiết/địa lý để lấy dữ liệu realtime.
- **Synthesis Agent:** Tổng hợp câu trả lời cuối cùng sử dụng Google Gemini LLM.

### 📚 Advanced RAG Pipeline
- **Ingestion:** Cắt nhỏ PDF, Markdown (Semantic Chunking) và lưu trữ dưới dạng Vector.
- **Retrieval:** Hybrid Search (Vector + Keyword) kết hợp Reranker giúp tăng độ chính xác của ngữ cảnh.

### 💻 Giao diện (Frontend)
- Web Application React + Vite.
- Giao diện trò chuyện trực quan với bong bóng chat hiện đại.
- Hiển thị nguồn trích dẫn tài liệu tham khảo (Sources) một cách minh bạch.

---

## Công nghệ

| Lớp | Công nghệ |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS |
| **Backend** | FastAPI, Python 3.9+ |
| **AI/LLM** | Google Gemini (google-genai), LangChain, SentenceTransformers |
| **Vector Database**| ChromaDB |
| **Infrastructure** | Docker, Docker Compose |

---

## Cài đặt & Triển khai (Khuyến nghị dùng Docker - Port 3001)

Dự án được tối ưu hóa để chạy dễ dàng bằng **Docker Compose** trên cổng **3001**:

```bash
# 1. Clone repository
git clone https://github.com/minhduc01168/rag-natural-disaster.git
cd rag-natural-disaster

# 2. Cấu hình biến môi trường
cp backend/.env.example backend/.env
# Chỉnh sửa file backend/.env và nhập GEMINI_API_KEY của bạn

# 3. Khởi chạy bằng Docker (Mặc định Port 3001)
docker compose up -d --build

# 4. Tự động nạp 7 tài liệu cẩm nang PCTT miền núi vào ChromaDB
docker compose exec backend python scripts/seed_knowledge_base.py
```

**Các dịch vụ sẽ chạy tại:**
- **Giao diện Web (Chatbot & GIS):** `http://localhost:3001` (hoặc `http://<IP_SERVER>:3001`)
- **Tài liệu API (Swagger):** `http://localhost:8000/docs`

> 📖 **Xem hướng dẫn chi tiết:**
> - [Hướng dẫn Triển khai & Mở Cổng Tường Lửa Port 3001](file:///home/mypc/rag-natural-disaster/DEPLOYMENT_GUIDE.md)
> - [Bộ Dữ liệu Chuẩn 100 Cặp QA (JSON & CSV)](file:///home/mypc/rag-natural-disaster/benchmark/README.md)

---

## Bộ Dữ liệu Chuẩn Đánh giá RAG (TERRA-100 Benchmark)

Hệ thống đi kèm bộ dữ liệu đánh giá thực nghiệm khoa học gồm **100 cặp QA chuẩn** trích xuất nguyên bản 100% (Verbatim Ground Truth) từ 7 tài liệu PCTT miền núi:
- 📄 **JSON Dataset**: [`benchmark/disaster_qa_benchmark_100.json`](file:///home/mypc/rag-natural-disaster/benchmark/disaster_qa_benchmark_100.json)
- 📊 **CSV Dataset (Excel UTF-8 BOM)**: [`benchmark/disaster_qa_benchmark_100.csv`](file:///home/mypc/rag-natural-disaster/benchmark/disaster_qa_benchmark_100.csv)
- 📜 **Tài liệu mô tả lược đồ & phân bố**: [`benchmark/README.md`](file:///home/mypc/rag-natural-disaster/benchmark/README.md)
- ⚙️ **Script kiểm định tính toàn vẹn 100%**: `python3 scripts/validate_benchmark_dataset.py`

---

## Cấu trúc dự án

Kiến trúc thư mục được tuân thủ nghiêm ngặt theo chuẩn Clean Architecture:

```
rag-natural-disaster/
├── benchmark/                   # ⭐ Bộ 100 cặp QA đánh giá RAG (JSON & CSV)
│   ├── disaster_qa_benchmark_100.json
│   ├── disaster_qa_benchmark_100.csv
│   └── README.md
├── frontend/                    # Giao diện Web (React + Vite, Port 3001)
│   └── src/
│       ├── config/api.ts        # Dynamic Base URL helper (Local / Server)
│       ├── components/chat/     # Component giao diện Chat
│       └── pages/               # Trang chính (TerraBotPage, GIS, Admin)
├── backend/                     # API Server (FastAPI, Port 8000)
│   ├── app/
│   │   ├── api/                 # Endpoint REST API
│   │   └── rag/                 # Lõi xử lý AI (Agents, Retrieval, Ingestion)
│   └── tests/                   # Kịch bản kiểm thử E2E và Unit Test
├── embedding_service/           # Microservice nhúng Harrier-OSS-v1-0.6B (Port 8002)
├── filtered_pdf_markdown/       # 7 tài liệu tri thức PCTT miền núi
├── scripts/                     # Scripts hỗ trợ (Seed, Validate, Benchmark, Paper Figures)
│   ├── seed_knowledge_base.py
│   ├── validate_benchmark_dataset.py
│   └── build_benchmark_dataset.py
├── DEPLOYMENT_GUIDE.md          # ⭐ Hướng dẫn triển khai & mở port chi tiết
└── docker-compose.yml           # Cấu hình Docker Compose đa dịch vụ
```

---

## API Documentation

Hệ thống RAG cung cấp endpoint duy nhất để tương tác với AI:

### `POST /api/v1/rag/chat`
**Payload (JSON):**
```json
{
  "query": "Làm thế nào để nhận biết dấu hiệu sạt lở đất?"
}
```

**Response (JSON):**
```json
{
  "answer": "Để nhận biết dấu hiệu sạt lở đất, bạn cần chú ý các hiện tượng sau...",
  "route_taken": "knowledge",
  "sources": [
    {
      "content": "Dấu hiệu nhận biết sạt lở: nước suối chuyển màu đục...",
      "metadata": { "source": "cam-nang-sat-lo.pdf", "page": 5 },
      "score": 0.85
    }
  ]
}
```

---

*Phát triển bởi đội ngũ TerraAlert - Ứng dụng Trí Tuệ Nhân Tạo bảo vệ cộng đồng.*
