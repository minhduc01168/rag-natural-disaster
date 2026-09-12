# -*- coding: utf-8 -*-
"""Master Benchmark Dataset Builder for Mountain Disaster Management.

Compiles 100 verified QA pairs from 7 mountain natural disaster knowledge base files
into standardized JSON and CSV formats for scientific RAG evaluation (RAGAS, TruLens, DeepEval).
"""

import csv
import json
import os
import sys

# Add repository root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.benchmark_data.doc1_0575 import DOC1_ITEMS
from scripts.benchmark_data.doc2_1ca1 import DOC2_ITEMS
from scripts.benchmark_data.doc3_30c1 import DOC3_ITEMS
from scripts.benchmark_data.doc4_7340 import DOC4_ITEMS
from scripts.benchmark_data.doc5_9b5c import DOC5_ITEMS
from scripts.benchmark_data.doc6_a351 import DOC6_ITEMS
from scripts.benchmark_data.doc7_a6cd import DOC7_ITEMS

OUTPUT_DIR = "backend/app/rag/evaluation/datasets"
JSON_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "disaster_qa_benchmark_100.json")
CSV_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "disaster_qa_benchmark_100.csv")

SOURCE_DOCS = [
    "0575f59d64e3407fa40049196cd01c5d.md",
    "1ca15953e77643e4bb2a63df40179a31.md",
    "30c127a0d6194029ae17dbc19131e2f4.md",
    "73408b097cb247f7954ae73dbfdce7e4.md",
    "9b5c5c224289412b880a70c4de27e23d.md",
    "a3515bb7de4f407c999b38eaad2be279.md",
    "a6cdc8f0e8ee43b19e884d0ee89d5474.md",
]

SCHEMA_FIELDS = [
    "id",
    "question",
    "ground_truth_context",
    "ground_truth_answer",
    "source_document",
    "category",
    "sub_category",
    "difficulty",
    "keywords",
]


def build_and_validate():
    print("=" * 75)
    print("  TERRA BENCHMARK: BUILDING MASTER QA DATASET (100 VERIFIED SAMPLES)")
    print("=" * 75)

    # 1. Aggregate all items
    all_items = (
        DOC1_ITEMS
        + DOC2_ITEMS
        + DOC3_ITEMS
        + DOC4_ITEMS
        + DOC5_ITEMS
        + DOC6_ITEMS
        + DOC7_ITEMS
    )

    total_count = len(all_items)
    print(f"\n[1/5] Total aggregated items: {total_count}")
    assert total_count == 100, f"Expected exactly 100 items, got {total_count}"

    # 2. Check and cache source markdown files
    print("\n[2/5] Reading 7 source markdown files for verbatim substring verification...")
    doc_cache = {}
    for filename in SOURCE_DOCS:
        path = os.path.join("filtered_pdf_markdown", filename)
        assert os.path.exists(path), f"File not found: {path}"
        with open(path, "r", encoding="utf-8") as f:
            doc_cache[filename] = f.read()
        print(f"  - Loaded {filename}: {len(doc_cache[filename]):,} chars")

    # 3. Comprehensive Integrity Validation
    print("\n[3/5] Validating all 100 QA pairs (Schema, Uniqueness, Exact Substring Match)...")
    seen_ids = set()
    seen_questions = set()

    for idx, item in enumerate(all_items, 1):
        # Schema field checks
        for k in SCHEMA_FIELDS:
            assert k in item, f"Item {idx} missing key '{k}'"
            val = item[k]
            assert val, f"Item {idx} key '{k}' has empty or null value: {val}"

        # Sequential ID check
        qa_id = item["id"]
        expected_id = f"TERRA_QA_{idx:03d}"
        assert qa_id == expected_id, f"Item {idx} ID mismatch: {qa_id} vs {expected_id}"
        assert qa_id not in seen_ids, f"Duplicate ID detected: {qa_id}"
        seen_ids.add(qa_id)

        # Unique question check
        q = item["question"].strip()
        assert q not in seen_questions, f"Duplicate question at {qa_id}: {q}"
        seen_questions.add(q)

        # Verbatim Context Substring check
        doc_filename = item["source_document"]
        assert doc_filename in doc_cache, f"Unknown source_document: {doc_filename}"
        source_text = doc_cache[doc_filename]
        ctx = item["ground_truth_context"]
        assert ctx in source_text, (
            f"FAIL: Ground truth context for {qa_id} is NOT a verbatim substring of {doc_filename}!"
        )

    print("  >>> SUCCESS: 100% of the 100 items passed exact substring & schema checks!")

    # 4. Save JSON dataset
    print("\n[4/5] Exporting datasets...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Exported JSON: {JSON_OUTPUT_PATH}")

    # 5. Save CSV dataset (with UTF-8-SIG for Microsoft Excel Vietnamese compatibility)
    csv_rows = []
    for item in all_items:
        row = dict(item)
        if isinstance(row.get("keywords"), list):
            row["keywords"] = ", ".join(row["keywords"])
        csv_rows.append(row)

    with open(CSV_OUTPUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_FIELDS)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"  [OK] Exported CSV (UTF-8 with BOM): {CSV_OUTPUT_PATH}")

    # 6. Print dataset statistical breakdown
    print("\n[5/5] Dataset Statistical Summary:")
    print("-" * 75)

    doc_dist = {}
    cat_dist = {}
    diff_dist = {}
    ctx_lens = []
    q_lens = []
    a_lens = []

    for it in all_items:
        doc_dist[it["source_document"]] = doc_dist.get(it["source_document"], 0) + 1
        cat_dist[it["category"]] = cat_dist.get(it["category"], 0) + 1
        diff_dist[it["difficulty"]] = diff_dist.get(it["difficulty"], 0) + 1
        ctx_lens.append(len(it["ground_truth_context"]))
        q_lens.append(len(it["question"]))
        a_lens.append(len(it["ground_truth_answer"]))

    print("\n1. Distribution by Source Document:")
    for d, c in sorted(doc_dist.items()):
        print(f"   * {d}: {c} items ({c}%)")

    print("\n2. Distribution by Research Category:")
    for ct, c in sorted(cat_dist.items(), key=lambda x: -x[1]):
        print(f"   * {ct}: {c} items ({c}%)")

    print("\n3. Distribution by Difficulty:")
    for df, c in sorted(diff_dist.items(), key=lambda x: -x[1]):
        print(f"   * {df}: {c} items ({c}%)")

    print("\n4. Length Metrics (Characters):")
    print(
        f"   * Ground Truth Context: min={min(ctx_lens):,} | max={max(ctx_lens):,} | avg={sum(ctx_lens)/len(ctx_lens):.1f} chars"
    )
    print(
        f"   * Question:             min={min(q_lens):,} | max={max(q_lens):,} | avg={sum(q_lens)/len(q_lens):.1f} chars"
    )
    print(
        f"   * Ground Truth Answer:  min={min(a_lens):,} | max={max(a_lens):,} | avg={sum(a_lens)/len(a_lens):.1f} chars"
    )

    print("\n" + "=" * 75)
    print("  TERRA BENCHMARK BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 75)


if __name__ == "__main__":
    build_and_validate()
