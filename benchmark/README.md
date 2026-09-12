# TERRA Mountain Disaster QA Benchmark Dataset (100 Verified QA Pairs)

## 1. Giới thiệu tổng quan (Dataset Overview)

**TERRA Mountain Disaster QA Benchmark 100** (`disaster_qa_benchmark_100.json` / `.csv`) là bộ dữ liệu chuẩn (Gold-standard Ground Truth Benchmark Dataset) được xây dựng phục vụ cho nghiên cứu khoa học và đánh giá thực nghiệm định lượng các hệ thống **Retrieval-Augmented Generation (RAG)** trong lĩnh vực phòng chống thiên tai tại các vùng miền núi Việt Nam.

Bộ dữ liệu được thiết kế nhằm đáp ứng đầy đủ các tiêu chuẩn đánh giá khắt khe của các framework tiên tiến như **RAGAS** (Context Recall, Context Precision, Faithfulness, Answer Relevance), **TruLens**, và **DeepEval**.

### Đặc điểm nổi bật (Key Highlights)
- **Quy mô**: Đúng **100 cặp QA** chuẩn hóa cao độ, bao phủ 7 tài liệu tri thức chuyên sâu trong kho tài liệu `filtered_pdf_markdown/`.
- **100% Verbatim Ground Truth**: 100/100 đoạn `ground_truth_context` đều là trích dẫn nguyên bản tuyệt đối (exact substring match) từ các tài liệu Markdown nguồn, triệt tiêu hoàn toàn rủi ro hallucination trong tập ground truth.
- **Tính toàn diện**: Bao phủ 6 nhóm chủ đề nghiên cứu trọng điểm từ thể chế pháp lý, cơ chế vật lý sạt lở, kỹ thuật chằng chống nhà cửa, đến kỹ năng sơ cấp cứu và bản đồ tác chiến ứng phó thiên tai.
- **Đa dạng định dạng xuất bản**:
  - `disaster_qa_benchmark_100.json`: Chuẩn machine-readable cho RAG pipeline và framework tự động.
  - `disaster_qa_benchmark_100.csv`: Chuẩn bảng mã UTF-8 with BOM (Byte Order Mark), hỗ trợ mở trực tiếp trên Microsoft Excel không lỗi font tiếng Việt.
  - `scripts/validate_benchmark_dataset.py`: Script tự động kiểm định tính toàn vẹn 100% dữ liệu trước khi chạy benchmark.

---

## 2. Nguồn tài liệu tri thức (Source Knowledge Corpus)

Bộ dữ liệu trích xuất từ 7 tài liệu nòng cốt trong thư mục `filtered_pdf_markdown/`:

| STT | File Markdown | Tên văn bản / Chuyên đề tri thức | Số câu QA | Tỷ lệ |
| :---: | :--- | :--- | :---: | :---: |
| 1 | `0575f59d64e3407fa40049196cd01c5d.md` | Tài liệu tập huấn PCTT cơ bản: Khái niệm hiểm họa/thảm họa, bão, ngập lụt, kỹ thuật chằng chống nhà ở, kỹ năng sơ cứu gãy xương/đuối nước | 12 | 12% |
| 2 | `1ca15953e77643e4bb2a63df40179a31.md` | Luật PCTT, QĐ 44 phân cấp rủi ro thiên tai, 8 vùng thiên tai, cơ chế hạn hán, rét hại sương muối | 16 | 16% |
| 3 | `30c127a0d6194029ae17dbc19131e2f4.md` | Sổ tay PCTT cấp xã: Cơ cấu BCH xã, 13 nhiệm vụ Chủ tịch UBND cấp xã, các giai đoạn phòng ngừa - ứng phó - khắc phục bão lũ, sạt lở | 14 | 14% |
| 4 | `73408b097cb247f7954ae73dbfdce7e4.md` | Sạt lở đất & lũ quét: Định nghĩa pháp lý QĐ 18/2021, cơ chế áp lực nước lỗ rỗng, phân vùng rủi ro Khu vực 1, an toàn bão cho trường học/doanh nghiệp, Đề án 553 | 20 | 20% |
| 5 | `9b5c5c224289412b880a70c4de27e23d.md` | Địa hình đồi núi Việt Nam, hướng núi TB-ĐN, thang Beaufort 6-12, mưa đá, túi cứu trợ khẩn cấp, nhận biết vết nứt sạt lở, cấm qua ngầm tràn, CBDRM | 18 | 18% |
| 6 | `a3515bb7de4f407c999b38eaad2be279.md` | Đặc điểm bão, lũ, lũ quét miền Trung (PGS.PTS. Lê Bắc Huỳnh), tổ hợp hình thế thời tiết cực đoan, giải pháp hiện đại hóa trạm quan trắc KTTV | 6 | 6% |
| 7 | `a6cdc8f0e8ee43b19e884d0ee89d5474.md` | Sổ tay phương án ứng phó theo cấp độ rủi ro (Dự án WB5/VN-Haz): Công thức UN-ISDR, phương châm 4 tại chỗ, nhóm dễ tổn thương, bản đồ tác chiến, vận hành hồ chứa | 14 | 14% |
| **Tổng** | **7 tài liệu tri thức** | **Toàn bộ kho tri thức phòng chống thiên tai miền núi** | **100** | **100%** |

---

## 3. Cấu trúc lược đồ dữ liệu (Dataset Schema)

Mỗi mẫu trong tập benchmark tuân thủ cấu trúc chuẩn 9 trường thông tin:

```json
{
  "id": "TERRA_QA_001",
  "question": "Theo tài liệu tập huấn phòng chống thiên tai, hiểm họa được định nghĩa như thế nào?",
  "ground_truth_context": "Là bất kỳ sự kiện, hiện tượng (do tự nhiên hoặc con người) có khả năng gây tổn thất đến tính mạng, tài sản và đời sống, gây thiệt hại về kinh tế, xã hội và tàn phá môi trường.\n\n> [MÔ TẢ HÌNH ẢNH]: ...",
  "ground_truth_answer": "Hiểm họa là bất kỳ sự kiện, hiện tượng (do tự nhiên hoặc con người gây ra) có khả năng gây tổn thất đến tính mạng, tài sản, đời sống, gây thiệt hại về kinh tế, xã hội và tàn phá môi trường (ví dụ như bão, áp thấp nhiệt đới, lũ lụt, lốc xoáy...).",
  "source_document": "0575f59d64e3407fa40049196cd01c5d.md",
  "category": "risk_assessment_mapping",
  "sub_category": "Định nghĩa và phân loại hiểm họa",
  "difficulty": "easy",
  "keywords": ["hiểm họa", "định nghĩa", "tự nhiên", "con người", "tổn thất", "bão lũ"]
}
```

### Chi tiết các trường:
- `id` *(string)*: Mã định danh duy nhất theo thứ tự tuần tự `TERRA_QA_001` đến `TERRA_QA_100`.
- `question` *(string)*: Câu hỏi chuẩn hóa bằng tiếng Việt tự nhiên, phản ánh đúng bài toán thực tế của người dân, cán bộ quản lý xã/huyện.
- `ground_truth_context` *(string)*: Đoạn ngữ cảnh căn cứ được trích xuất nguyên bản từ tài liệu nguồn Markdown (phục vụ tính toán **Context Recall** và **Context Precision**).
- `ground_truth_answer` *(string)*: Câu trả lời mẫu chuẩn xác, cô đọng nhưng đầy đủ các luận điểm khoa học và quy định pháp lý (phục vụ tính toán **Faithfulness** và **Answer Relevance / Answer Semantic Similarity**).
- `source_document` *(string)*: Tên file Markdown nguồn chứa ngữ cảnh.
- `category` *(string)*: Nhóm chủ đề nghiên cứu (6 phân lớp khoa học).
- `sub_category` *(string)*: Tiểu mục nội dung chuyên sâu.
- `difficulty` *(string)*: Độ khó câu hỏi (`easy`: tra cứu trực tiếp; `medium`: tổng hợp thông tin; `hard`: phân tích bảng số liệu, nhiều bước logic hoặc tình huống phức tạp).
- `keywords` *(list[string])*: Danh sách các từ khóa trọng tâm phục vụ kiểm thử hybrid search (BM25 keyword search).

---

## 4. Thống kê bộ dữ liệu (Statistical Profile)

### 4.1. Phân bố theo Nhóm chủ đề nghiên cứu (Research Categories)
| Nhóm chủ đề | Mã category | Số lượng | Tỷ lệ |
| :--- | :--- | :---: | :---: |
| Quản trị và ứng phó cấp cộng đồng | `community_governance` | 26 | 26% |
| Đánh giá và lập bản đồ rủi ro thiên tai | `risk_assessment_mapping` | 18 | 18% |
| Bão, ngập lụt và thời tiết cực đoan | `typhoon_flood` | 18 | 18% |
| Lũ quét, sạt lở đất miền núi | `landslide_flashflood` | 18 | 18% |
| Sơ cứu chấn thương và sinh tồn khẩn cấp | `first_aid_survival` | 18 | 18% |
| Sơ tán và bảo vệ nhóm dễ bị tổn thương | `vulnerability_evacuation` | 2 | 2% |
| **Tổng cộng** | **6 nhóm** | **100** | **100%** |

### 4.2. Phân bố theo Độ khó (Difficulty)
- **Easy (28%)**: 28 câu hỏi trích xuất sự kiện, định nghĩa cơ bản, quy định định tính trực tiếp.
- **Medium (56%)**: 56 câu hỏi tổng hợp quy trình (4 tại chỗ, sơ tán, chằng chống nhà, phân vùng thiên tai, quy tắc cứu hộ).
- **Hard (16%)**: 16 câu hỏi đối chiếu số liệu bảng biểu (cấp độ rủi ro, thang Beaufort, vận tốc gió km/h, cơ chế áp lực lỗ rỗng, tổ hợp hình thế thời tiết lịch sử).

### 4.3. Chỉ số độ dài (Length Metrics)
| Thành phần | Độ dài tối thiểu | Độ dài tối đa | Độ dài trung bình |
| :--- | :---: | :---: | :---: |
| **Question** | 68 ký tự | 171 ký tự | **111.9 ký tự** |
| **Ground Truth Answer** | 182 ký tự | 703 ký tự | **360.3 ký tự** |
| **Ground Truth Context** | 89 ký tự | 86,098 ký tự | **2,177.8 ký tự** |

---

## 5. Hướng dẫn sử dụng cho đánh giá RAG (Usage in RAG Evaluation)

### 5.1. Chạy kiểm định tính toàn vẹn (Integrity Check)
Trước khi chạy bất kỳ thực nghiệm nào, chạy script sau để kiểm tra:
```bash
python3 scripts/validate_benchmark_dataset.py
```

### 5.2. Đọc dữ liệu vào Python và Pandas
```python
import pandas as pd
import json

# Cách 1: Đọc bằng JSON
with open("backend/app/rag/evaluation/datasets/disaster_qa_benchmark_100.json", "r", encoding="utf-8") as f:
    benchmark_data = json.load(f)

# Cách 2: Đọc bằng Pandas DataFrame từ CSV
df = pd.read_csv("backend/app/rag/evaluation/datasets/disaster_qa_benchmark_100.csv", encoding="utf-8-sig")
print(f"Loaded {len(df)} samples successfully!")
```

### 5.3. Tích hợp với RAGAS
```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_recall,
    context_precision
)

# Chuyển đổi dữ liệu sang Hugging Face Dataset theo format RAGAS:
ragas_data = {
    "question": [item["question"] for item in benchmark_data],
    "ground_truth": [item["ground_truth_answer"] for item in benchmark_data],
    "ground_truth_contexts": [[item["ground_truth_context"]] for item in benchmark_data],
    # Sau khi chạy pipeline RAG của bạn, điền 2 mảng này:
    # "answer": [...],
    # "contexts": [[...], ...]
}
```

---

## 6. Cam kết Liêm chính học thuật (Academic Integrity)

1. **Khách quan và có thể tái lập (Reproducibility)**: Toàn bộ mã nguồn tạo bộ benchmark (`scripts/build_benchmark_dataset.py`) và kiểm tra tự động (`scripts/validate_benchmark_dataset.py`) được lưu trữ nguyên vẹn trong repository.
2. **Không rò rỉ dữ liệu (No Data Leakage)**: Bộ câu hỏi được biên soạn độc lập dựa trên tri thức chuyên gia từ tài liệu chuẩn, không sử dụng kết quả sinh tự động từ LLM khi chưa qua kiểm duyệt.
3. **Phù hợp nghiên cứu công bố quốc tế**: Cấu trúc dữ liệu và bảng phân bố chỉ số có thể trích xuất trực tiếp đưa vào phần *Experimental Setup / Benchmark Construction* của bài báo khoa học.
