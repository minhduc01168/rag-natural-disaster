from app.core.celery_app import celery_app
from datetime import datetime
import time


@celery_app.task(bind=True, name="tasks.fetch_weather_data")
def fetch_weather_data(self, lat: float, lon: float):
    """
    Fetch weather data for a specific location.
    This is a placeholder - will be connected to real API.
    """
    try:
        # Simulate API call
        time.sleep(1)
        
        return {
            "status": "success",
            "data": {
                "latitude": lat,
                "longitude": lon,
                "temperature": 28.5,
                "humidity": 75,
                "wind_speed": 12,
                "condition": "Nhiều mây",
            },
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, name="tasks.process_alert")
def process_alert(self, alert_data: dict):
    """
    Process and store alert data.
    """
    try:
        # Simulate processing
        time.sleep(0.5)
        
        return {
            "status": "processed",
            "alert_id": alert_data.get("id"),
            "processed_at": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=30)


@celery_app.task(bind=True, name="tasks.cleanup_old_data")
def cleanup_old_data(self, days_old: int = 30):
    """
    Clean up data older than specified days.
    """
    try:
        # Simulate cleanup
        time.sleep(2)
        
        return {
            "status": "cleaned",
            "deleted_count": 0,
            "days_threshold": days_old,
            "cleaned_at": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=300)
