from fastapi import APIRouter

from app.api.rag_router import router as rag_router
from app.api.fast_lane_router import router as fast_lane_router
from app.api.auth_router import router as auth_router
from app.api.admin_rag_router import router as admin_rag_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(rag_router, prefix="/rag", tags=["Agentic RAG"])
api_router.include_router(fast_lane_router, prefix="/fast-lane", tags=["Fast Lane"])
api_router.include_router(admin_rag_router, prefix="/admin/rag", tags=["Admin RAG"])
