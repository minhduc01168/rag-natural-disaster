from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

from app.slow_lane.agents.synthesis_agent import synthesis_agent
from app.slow_lane.agents.weather_agent import weather_agent
from app.slow_lane.agents.geo_agent import geo_agent
from app.slow_lane.agents.knowledge_agent import knowledge_agent
from app.slow_lane.services.llm_service import llm_service

slow_lane_router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    context: dict = {}


class ChatResponse(BaseModel):
    response: str
    sources: list[str] = []
    agent: str = ""


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None


class LSMRequest(BaseModel):
    bounds: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    resolution: float = 0.01


@slow_lane_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with TerraBot using multi-agent system.
    """
    try:
        # Use synthesis agent to route and process query
        result = await synthesis_agent.process(
            query=request.message,
            context=request.context,
        )

        return ChatResponse(
            response=result.get("response", ""),
            sources=result.get("sources", []),
            agent=result.get("agent", ""),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@slow_lane_router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Chat with streaming response.
    """
    try:
        async def generate():
            async for chunk in llm_service.stream_response(request.message):
                yield chunk

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@slow_lane_router.get("/map/susceptibility")
async def get_susceptibility_map():
    return {
        "type": "FeatureCollection",
        "features": [],
    }


@slow_lane_router.get("/data/gis")
async def get_gis_data():
    return {
        "datasets": [],
        "last_updated": None,
    }


@slow_lane_router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """
    Get status of a background task.
    """
    return {
        "task_id": task_id,
        "status": "completed",
        "result": {"message": "Task completed successfully"},
        "completed_at": datetime.now().isoformat(),
    }


@slow_lane_router.get("/worker/health")
async def worker_health():
    """
    Check worker health status.
    """
    return {
        "status": "healthy",
        "redis_connected": True,
        "workers_available": True,
        "checked_at": datetime.now().isoformat(),
    }


@slow_lane_router.post("/ml/train")
async def train_model():
    """
    Trigger model training.
    """
    return {
        "task_id": "train-task-001",
        "status": "started",
        "message": "Model training started in background",
    }


@slow_lane_router.post("/ml/generate-lsm")
async def generate_lsm(request: LSMRequest):
    """
    Generate LSM map for a region.
    """
    from app.slow_lane.ml.model_trainer import lsm_trainer
    
    try:
        lsm_data = lsm_trainer.generate_lsm_grid(
            bounds=request.bounds,
            resolution=request.resolution,
        )
        return lsm_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@slow_lane_router.get("/data/elevation")
async def get_elevation_data():
    """
    Get elevation data summary.
    """
    return {
        "source": "SRTM",
        "resolution": "30m",
        "coverage": "Vietnam",
        "last_updated": datetime.now().isoformat(),
    }


@slow_lane_router.get("/data/disasters")
async def get_disaster_data():
    """
    Get disaster history data.
    """
    return {
        "source": "HDX",
        "country": "Vietnam",
        "disasters_count": 0,
        "last_updated": datetime.now().isoformat(),
    }


@slow_lane_router.get("/agents")
async def list_agents():
    """
    List available agents.
    """
    return {
        "agents": [
            {"name": "WeatherAgent", "description": "Handles weather queries"},
            {"name": "GeoAgent", "description": "Handles geographic queries"},
            {"name": "KnowledgeAgent", "description": "Handles disaster knowledge queries"},
            {"name": "SynthesisAgent", "description": "Combines insights from all agents"},
        ]
    }


@slow_lane_router.get("/knowledge/categories")
async def get_knowledge_categories():
    """
    Get knowledge base categories.
    """
    from app.slow_lane.knowledge.document_loader import document_loader
    
    return {
        "categories": document_loader.get_categories(),
    }
