from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.fast_lane.services.weather_service import get_weather_from_meteostat
from app.fast_lane.services.alert_engine import classify_weather
from app.fast_lane.services.notification_service import notification_manager
from app.fast_lane.models.alert import AlertResponse

fast_lane_router = APIRouter()


class SOSRequest(BaseModel):
    latitude: float
    longitude: float
    message: str = ""
    phone: str = ""


class SOSResponse(BaseModel):
    status: str
    message: str
    ticket_id: str


class AlertItem(BaseModel):
    id: str
    level: str
    location: str
    description: str
    timestamp: datetime


class AlertsResponse(BaseModel):
    alerts: List[AlertItem]
    count: int


@fast_lane_router.post("/sos", response_model=SOSResponse)
async def create_sos(request: SOSRequest):
    return SOSResponse(
        status="received",
        message="Tín hiệu SOS đã được ghi nhận. Đội cứu nạn sẽ liên hệ sớm.",
        ticket_id="SOS-2026-001",
    )


@fast_lane_router.get("/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
    weather_data = await get_weather_from_meteostat(lat, lon)
    if weather_data:
        # Classify weather into alert level
        alert = classify_weather(
            temperature=weather_data.temperature,
            humidity=weather_data.humidity,
            wind_speed=weather_data.wind_speed,
            rainfall=weather_data.rainfall or 0.0,
        )
        return {
            "status": "success",
            "data": weather_data.model_dump(),
            "alert": alert.model_dump(),
        }
    return {
        "status": "error",
        "message": "Không thể lấy dữ liệu thời tiết",
    }


@fast_lane_router.get("/alerts")
async def get_alerts():
    return AlertsResponse(
        alerts=[],
        count=0,
    )


@fast_lane_router.get("/alert-level")
async def get_alert_level(
    temperature: float = 25.0,
    humidity: float = 70.0,
    wind_speed: float = 10.0,
    rainfall: float = 0.0,
):
    """
    Get alert level based on weather parameters.
    Useful for testing and direct classification.
    """
    alert = classify_weather(temperature, humidity, wind_speed, rainfall)
    return alert.model_dump()


@fast_lane_router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """
    WebSocket endpoint for real-time alert notifications.
    Clients connect here to receive live alerts.
    """
    await notification_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            # Client can send ping/pong or request specific data
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        notification_manager.disconnect(websocket)


@fast_lane_router.get("/ws/status")
async def websocket_status():
    """Get WebSocket connection status."""
    return {
        "active_connections": notification_manager.connection_count,
    }
