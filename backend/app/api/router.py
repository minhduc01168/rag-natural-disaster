from fastapi import APIRouter

from app.api.rag_router import router as rag_router
from app.api.gis_router import gis_router

api_router = APIRouter()

api_router.include_router(rag_router, prefix="/rag", tags=["Agentic RAG"])
api_router.include_router(gis_router, prefix="/gis", tags=["GIS Data"])
