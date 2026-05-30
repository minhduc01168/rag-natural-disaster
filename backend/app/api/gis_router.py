from fastapi import APIRouter, Query
from typing import Optional, List
from app.slow_lane.services.geojson_service import geojson_service

gis_router = APIRouter()


# Mock data for demonstration
MOCK_ELEVATION = [
    {"lat": 21.0 + i * 0.01, "lon": 105.8 + i * 0.01, "elevation": 100 + i * 10, "source": "srtm"}
    for i in range(50)
]

MOCK_PRECIPITATION = [
    {"lat": 21.0 + i * 0.01, "lon": 105.8 + i * 0.01, "amount": 5.0 + i * 0.5, "date": f"2026-01-{i+1:02d}", "source": "gpm"}
    for i in range(30)
]

MOCK_DISASTERS = [
    {"lat": 21.02, "lon": 105.85, "type": "flood", "severity": "high", "date": "2025-08-15", "description": "Lũ lụt Yên Bái"},
    {"lat": 22.34, "lon": 103.84, "type": "landslide", "severity": "medium", "date": "2025-09-01", "description": "Sạt lở Lào Cai"},
    {"lat": 16.05, "lon": 108.22, "type": "typhoon", "severity": "high", "date": "2025-10-10", "description": "Bão Đà Nẵng"},
]

MOCK_LSM = [
    {"lat": 21.0 + i * 0.05, "lon": 105.8 + i * 0.05, "susceptibility": 0.3 + i * 0.01, "risk_level": "low" if i < 10 else "medium" if i < 20 else "high", "model_version": "v1"}
    for i in range(30)
]


@gis_router.get("/elevation")
async def get_elevation(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=1000),
):
    """
    Get elevation data as GeoJSON.
    """
    bbox_list = None
    if bbox:
        try:
            bbox_list = [float(x) for x in bbox.split(",")]
        except ValueError:
            pass

    return geojson_service.elevation_to_geojson(
        data=MOCK_ELEVATION,
        bbox=bbox_list,
        page=page,
        per_page=per_page,
    )


@gis_router.get("/precipitation")
async def get_precipitation(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=1000),
):
    """
    Get precipitation data as GeoJSON.
    """
    bbox_list = None
    if bbox:
        try:
            bbox_list = [float(x) for x in bbox.split(",")]
        except ValueError:
            pass

    return geojson_service.precipitation_to_geojson(
        data=MOCK_PRECIPITATION,
        bbox=bbox_list,
        page=page,
        per_page=per_page,
    )


@gis_router.get("/disasters")
async def get_disasters(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    type: Optional[str] = Query(None, description="Disaster type filter"),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=1000),
):
    """
    Get disaster history as GeoJSON.
    """
    bbox_list = None
    if bbox:
        try:
            bbox_list = [float(x) for x in bbox.split(",")]
        except ValueError:
            pass

    filtered_data = MOCK_DISASTERS
    if type:
        filtered_data = [d for d in MOCK_DISASTERS if d["type"] == type]

    return geojson_service.disasters_to_geojson(
        data=filtered_data,
        bbox=bbox_list,
        page=page,
        per_page=per_page,
    )


@gis_router.get("/lsm")
async def get_lsm(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    risk_level: Optional[str] = Query(None, description="Risk level filter: low, medium, high"),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=1000),
):
    """
    Get LSM predictions as GeoJSON.
    """
    bbox_list = None
    if bbox:
        try:
            bbox_list = [float(x) for x in bbox.split(",")]
        except ValueError:
            pass

    filtered_data = MOCK_LSM
    if risk_level:
        filtered_data = [d for d in MOCK_LSM if d["risk_level"] == risk_level]

    return geojson_service.lsm_to_geojson(
        data=filtered_data,
        bbox=bbox_list,
        page=page,
        per_page=per_page,
    )


@gis_router.get("/summary")
async def get_gis_summary():
    """
    Get summary of available GIS data.
    """
    return {
        "elevation": {"count": len(MOCK_ELEVATION), "source": "SRTM"},
        "precipitation": {"count": len(MOCK_PRECIPITATION), "source": "GPM"},
        "disasters": {"count": len(MOCK_DISASTERS), "source": "HDX"},
        "lsm": {"count": len(MOCK_LSM), "source": "ML Model"},
    }
