import os
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from app.api.deps import get_current_admin_user
from app.rag.ingestion.parser import MasterDocumentParser
from app.rag.ingestion.chunker import SemanticChunker
from app.rag.ingestion.vector_store import ChromaManager

router = APIRouter()

master_parser = MasterDocumentParser()
chunker = SemanticChunker()
chroma_manager = ChromaManager()

class ChunkData(BaseModel):
    text: str
    metadata: Dict[str, Any]

class CommitRequest(BaseModel):
    chunks: List[ChunkData]

@router.post("/dry-run", response_model=List[ChunkData])
async def dry_run_ingestion(
    file: UploadFile = File(...),
    admin = Depends(get_current_admin_user)
):
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Bước 1: Phân tích tài liệu
        extracted_text = master_parser.route_and_parse(tmp_path)
        
        os.unlink(tmp_path)

        # Bước 2: Cắt mảnh (Chunking)
        docs = chunker.chunk_text(extracted_text)
        
        result = []
        for doc in docs:
            result.append(ChunkData(
                text=doc.page_content,
                metadata=doc.metadata
            ))
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
    admin = Depends(get_current_admin_user)
):
    try:
        docs = [DummyDoc(c.text, c.metadata) for c in request.chunks]
        chroma_manager.add_documents(docs)
        return {"status": "success", "inserted": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
