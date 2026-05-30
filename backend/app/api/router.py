from fastapi import APIRouter

from app.fast_lane.router import fast_lane_router
from app.slow_lane.router import slow_lane_router
from app.api.gis_router import gis_router

api_router = APIRouter()

api_router.include_router(fast_lane_router, prefix="/fast-lane", tags=["Fast Lane"])
api_router.include_router(slow_lane_router, prefix="/slow-lane", tags=["Slow Lane"])
api_router.include_router(gis_router, prefix="/gis", tags=["GIS Data"])
