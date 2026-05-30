import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime

from app.main import app
from app.fast_lane.models.weather import WeatherData
from app.fast_lane.models.alert import AlertLevel
from app.fast_lane.services.alert_engine import classify_weather
from app.fast_lane.services.notification_service import NotificationManager
from app.slow_lane.services.data_normalizer import data_normalizer
from app.slow_lane.ml.model_trainer import lsm_trainer

client = TestClient(app)


# ==================== System Tests ====================

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TerraAlert API"
    assert data["status"] == "running"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ==================== Fast Lane Tests ====================

def test_create_sos():
    response = client.post(
        "/api/v1/fast-lane/sos",
        json={
            "latitude": 21.0285,
            "longitude": 105.8542,
            "message": "Cần cứu trợ khẩn cấp",
            "phone": "0123456789",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"


@patch("app.fast_lane.services.weather_service.get_weather_from_meteostat")
def test_get_weather_success(mock_get_weather):
    mock_get_weather.return_value = WeatherData(
        temperature=28.5,
        humidity=75.0,
        wind_speed=12.0,
        condition="Nhiều mây",
        location_name="Vị trí (21.03, 105.85)",
        latitude=21.0285,
        longitude=105.8542,
        timestamp=datetime.now(),
        rainfall=0.0,
    )
    response = client.get("/api/v1/fast-lane/weather/21.0285/105.8542")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_get_alerts():
    response = client.get("/api/v1/fast-lane/alerts")
    assert response.status_code == 200


# ==================== Alert Engine Tests ====================

def test_alert_level_green():
    alert = classify_weather(temperature=25.0, humidity=60.0, wind_speed=10.0, rainfall=5.0)
    assert alert.level == AlertLevel.GREEN


def test_alert_level_yellow():
    alert = classify_weather(temperature=38.0, humidity=60.0, wind_speed=10.0, rainfall=0.0)
    assert alert.level == AlertLevel.YELLOW


def test_alert_level_red():
    alert = classify_weather(temperature=45.0, humidity=60.0, wind_speed=10.0, rainfall=0.0)
    assert alert.level == AlertLevel.RED


# ==================== Slow Lane Tests ====================

def test_chat():
    response = client.post(
        "/api/v1/slow-lane/chat",
        json={"message": "Xin chào"},
    )
    assert response.status_code == 200


def test_get_susceptibility_map():
    response = client.get("/api/v1/slow-lane/map/susceptibility")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"


def test_task_status():
    response = client.get("/api/v1/slow-lane/tasks/test-task-001")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "status" in data


def test_worker_health():
    response = client.get("/api/v1/slow-lane/worker/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# ==================== ML Tests ====================

def test_generate_lsm():
    response = client.post(
        "/api/v1/slow-lane/ml/generate-lsm",
        json={
            "bounds": [105.0, 20.0, 106.0, 21.0],
            "resolution": 0.1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert "features" in data


def test_lsm_trainer_grid():
    lsm_data = lsm_trainer.generate_lsm_grid(
        bounds=[105.0, 20.0, 106.0, 21.0],
        resolution=0.5,
    )
    assert lsm_data["type"] == "FeatureCollection"
    assert len(lsm_data["features"]) > 0


# ==================== Data Normalizer Tests ====================

def test_normalize_elevation():
    raw_data = {
        "records": [
            {"lat": 21.0, "lon": 105.8, "elevation": 100},
            {"lat": 21.1, "lon": 105.9, "elevation": 150},
        ]
    }
    records = data_normalizer.normalize_elevation(raw_data)
    assert len(records) == 2
    assert "geom" in records[0]
    assert "elevation" in records[0]


def test_normalize_disasters():
    raw_data = [
        {
            "type": "flood",
            "severity": "high",
            "date": "2025-08-15",
            "coordinates": {"lat": 21.72, "lon": 104.87},
        }
    ]
    records = data_normalizer.normalize_disasters(raw_data)
    assert len(records) == 1
    assert records[0]["type"] == "flood"


def test_validate_geometry():
    assert data_normalizer.validate_geometry("POINT(105.8 21.0)") == True
    assert data_normalizer.validate_geometry("INVALID") == False
    assert data_normalizer.validate_geometry("") == False


# ==================== GIS Data Tests ====================

def test_get_elevation_data():
    response = client.get("/api/v1/slow-lane/data/elevation")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "SRTM"


def test_get_disaster_data():
    response = client.get("/api/v1/slow-lane/data/disasters")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "HDX"
