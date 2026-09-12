# -*- coding: utf-8 -*-
"""Knowledge Base Seeder for Mountain Disaster Management.

Parses and ingests the 7 core mountain disaster documents from `filtered_pdf_markdown/`
into ChromaDB using SemanticChunker (MarkdownHeaderTextSplitter + RecursiveCharacterTextSplitter).
Works both locally and inside Docker / production environment.
"""

import argparse
import os
import sys
import time

# Ensure app package is accessible
sys.path.append(os.path.abspath("backend"))
sys.path.append(os.path.abspath("."))

from app.rag.ingestion.chunker import SemanticChunker
from app.rag.ingestion.vector_store import ChromaManager

SOURCE_DIR = "filtered_pdf_markdown"

DOCUMENTS = [
    ("0575f59d64e3407fa40049196cd01c5d.md", "Tài liệu tập huấn PCTT cơ bản"),
    ("1ca15953e77643e4bb2a63df40179a31.md", "Luật PCTT & Phân vùng rủi ro thiên tai"),
    ("30c127a0d6194029ae17dbc19131e2f4.md", "Sổ tay PCTT cấp xã"),
    ("73408b097cb247f7954ae73dbfdce7e4.md", "Lũ quét & Sạt lở đất"),
    ("9b5c5c224289412b880a70c4de27e23d.md", "Địa hình đồi núi & Thang Beaufort"),
    ("a3515bb7de4f407c999b38eaad2be279.md", "Thiên tai bão lũ miền Trung"),
    ("a6cdc8f0e8ee43b19e884d0ee89d5474.md", "Sổ tay WB5 ứng phó theo cấp độ rủi ro"),
]


def seed_knowledge_base(collection_name: str = "disaster_knowledge", reset: bool = False, batch_size: int = 50):
    print("=" * 75)
    print(f"  TERRA: SEEDING KNOWLEDGE BASE -> Collection: '{collection_name}'")
    print("=" * 75)

    chroma_mgr = ChromaManager(collection_name=collection_name)

    if reset:
        print(f"[Reset] Deleting existing collection '{collection_name}'...")
        try:
            chroma_mgr.client.delete_collection(collection_name)
            print(f"[Reset] Deleted collection '{collection_name}'. Recreating...")
            chroma_mgr.collection = chroma_mgr.client.get_or_create_collection(
                name=collection_name,
                embedding_function=chroma_mgr.embedding_fn
            )
        except Exception as e:
            print(f"[Reset] Notice: {e}")

    chunker = SemanticChunker(chunk_size=1000, chunk_overlap=150)
    total_docs_processed = 0
    total_chunks_created = 0
    start_time = time.time()

    for filename, title in DOCUMENTS:
        filepath = os.path.join(SOURCE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[Warning] File not found: {filepath}, skipping...")
            continue

        print(f"\n[Processing] {title} ({filename})...")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunker.chunk_text(content)
        print(f"  - Parsed {len(content):,} chars into {len(chunks)} chunks.")

        # Enrich chunk metadata
        for i, chunk in enumerate(chunks):
            if not hasattr(chunk, "metadata") or chunk.metadata is None:
                chunk.metadata = {}
            chunk.metadata["source"] = filename
            chunk.metadata["document_title"] = title
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)

        # Ingest in batches to avoid overwhelming the embedding service
        for b_idx in range(0, len(chunks), batch_size):
            batch = chunks[b_idx : b_idx + batch_size]
            print(f"  - Ingesting batch {b_idx // batch_size + 1}/{(len(chunks) - 1) // batch_size + 1} ({len(batch)} chunks)...")
            chroma_mgr.add_documents(batch)

        total_docs_processed += 1
        total_chunks_created += len(chunks)

    elapsed = time.time() - start_time
    print("\n" + "=" * 75)
    print(f"  SEEDING COMPLETED SUCCESSFULLY!")
    print(f"  * Total documents ingested: {total_docs_processed}/{len(DOCUMENTS)}")
    print(f"  * Total chunks stored:    {total_chunks_created:,}")
    print(f"  * Total time elapsed:     {elapsed:.1f}s")
    print("=" * 75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed 7 Mountain Disaster documents into ChromaDB.")
    parser.add_argument("--collection", type=str, default="disaster_knowledge", help="ChromaDB collection name")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate the collection before seeding")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for embedding calls")
    args = parser.parse_args()

    seed_knowledge_base(collection_name=args.collection, reset=args.reset, batch_size=args.batch_size)
