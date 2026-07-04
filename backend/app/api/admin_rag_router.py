import os
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.api.deps import get_current_admin_user
from app.rag.ingestion.parser import MasterDocumentParser
from app.rag.ingestion.chunker import SemanticChunker
from app.rag.ingestion.vector_store import ChromaManager

router = APIRouter()

master_parser = MasterDocumentParser()
chunker = SemanticChunker()
chroma_manager = ChromaManager()


# ─────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────

class ChunkData(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: Dict[str, Any]


class CommitRequest(BaseModel):
    chunks: List[ChunkData]


class DocumentInfo(BaseModel):
    filename: str
    chunk_count: int
    status: str = "ready"  # "ready" | "processing" | "failed"


# ─────────────────────────────────────────────
# Ingestion endpoints
# ─────────────────────────────────────────────

@router.post("/dry-run", response_model=List[ChunkData])
async def dry_run_ingestion(
    file: UploadFile = File(...),
    admin=Depends(get_current_admin_user),
):
    """Phân tích và chunk tài liệu — chưa lưu vào DB."""
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        extracted_text = master_parser.route_and_parse(tmp_path)
        os.unlink(tmp_path)

        docs = chunker.chunk_text(extracted_text)

        result = []
        for doc in docs:
            meta = dict(doc.metadata) if doc.metadata else {}
            meta["source_file"] = file.filename
            result.append(ChunkData(text=doc.page_content, metadata=meta))
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class DummyDoc:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata


@router.post("/commit")
async def commit_ingestion(
    request: CommitRequest,
    admin=Depends(get_current_admin_user),
):
    """Lưu các chunks đã duyệt vào ChromaDB."""
    try:
        docs = []
        for c in request.chunks:
            meta = dict(c.metadata) if c.metadata else {}
            meta["status"] = "ready"
            docs.append(DummyDoc(c.text, meta))
        chroma_manager.add_documents(docs)
        return {"status": "success", "inserted": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# KB Documents dashboard endpoints
# ─────────────────────────────────────────────

@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents(
    admin=Depends(get_current_admin_user),
):
    """
    Trả danh sách tất cả tài liệu đã upload (unique theo source_file),
    kèm số chunks mỗi file.
    """
    try:
        all_data = chroma_manager.get_all_documents()
        metadatas: list = all_data.get("metadatas", []) or []

        # Đếm chunks theo source_file và kiểm tra status
        count: Dict[str, int] = {}
        status_map: Dict[str, str] = {}
        for meta in metadatas:
            src = (meta or {}).get("source_file", "unknown")
            count[src] = count.get(src, 0) + 1
            st = (meta or {}).get("status", "ready")
            status_map[src] = st

        return [
            DocumentInfo(filename=fname, chunk_count=cnt, status=status_map.get(fname, "ready"))
            for fname, cnt in sorted(count.items())
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/{filename:path}/chunks", response_model=List[ChunkData])
async def get_document_chunks(
    filename: str,
    admin=Depends(get_current_admin_user),
):
    """
    Trả toàn bộ chunks của một tài liệu cụ thể,
    lọc theo source_file trong metadata.
    """
    try:
        all_data = chroma_manager.get_all_documents()
        ids: list       = all_data.get("ids", []) or []
        documents: list = all_data.get("documents", []) or []
        metadatas: list = all_data.get("metadatas", []) or []

        chunks = []
        for i, meta in enumerate(metadatas):
            src = (meta or {}).get("source_file", "")
            if src == filename:
                chunks.append(ChunkData(
                    id=ids[i] if i < len(ids) else None,
                    text=documents[i] if i < len(documents) else "",
                    metadata=meta or {},
                ))
        return chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{filename:path}")
async def delete_document(
    filename: str,
    admin=Depends(get_current_admin_user),
):
    """Xóa toàn bộ chunks của một tài liệu khỏi ChromaDB."""
    try:
        all_data = chroma_manager.get_all_documents()
        ids: list       = all_data.get("ids", []) or []
        metadatas: list = all_data.get("metadatas", []) or []

        ids_to_delete = [
            ids[i]
            for i, meta in enumerate(metadatas)
            if (meta or {}).get("source_file", "") == filename and i < len(ids)
        ]

        if not ids_to_delete:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy tài liệu: {filename}")

        chroma_manager.collection.delete(ids=ids_to_delete)
        return {"status": "success", "deleted": len(ids_to_delete), "filename": filename}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
