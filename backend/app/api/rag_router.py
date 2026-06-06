from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.rag.agents.synthesis_agent import SynthesisAgent

router = APIRouter()

# Khởi tạo agent dùng chung cho router, có thể chuyển llm_mock=False trong môi trường Production
synthesis_agent = SynthesisAgent(llm_mock=True)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    route_taken: str
    answer: str
    sources: List[str]

@router.post("/chat", response_model=QueryResponse)
async def chat_with_agent(request: QueryRequest):
    """
    Endpoint chính để trò chuyện với Agentic RAG System.
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        result = synthesis_agent.process_query(request.query)
        
        return QueryResponse(
            query=result["query"],
            route_taken=result["route_taken"],
            answer=result["answer"],
            sources=result["sources"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
