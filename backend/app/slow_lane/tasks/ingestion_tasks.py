from app.core.celery_app import celery_app
from datetime import datetime
import time


@celery_app.task(bind=True, name="tasks.fetch_srtm_data")
def fetch_srtm_data(self, region: dict):
    """
    Fetch SRTM elevation data from Google Earth Engine.
    """
    try:
        # Simulate GEE API call
        time.sleep(3)
        
        return {
            "status": "success",
            "data_type": "srtm",
            "region": region,
            "records_count": 1000,
            "fetched_at": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=120)


@celery_app.task(bind=True, name="tasks.fetch_sentinel2_data")
def fetch_sentinel2_data(self, region: dict, date_range: dict):
    """
    Fetch Sentinel-2 satellite imagery metadata.
    """
    try:
        # Simulate GEE API call
        time.sleep(5)
        
        return {
            "status": "success",
            "data_type": "sentinel2",
            "region": region,
            "date_range": date_range,
            "images_count": 15,
            "fetched_at": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=180)


@celery_app.task(bind=True, name="tasks.fetch_gpm_data")
def fetch_gpm_data(self, region: dict, start_date: str, end_date: str):
    """
    Fetch GPM precipitation data.
    """
    try:
        # Simulate GEE API call
        time.sleep(4)
        
        return {
            "status": "success",
            "data_type": "gpm",
            "region": region,
            "start_date": start_date,
            "end_date": end_date,
            "records_count": 365,
            "fetched_at": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=120)


@celery_app.task(bind=True, name="tasks.fetch_hdx_data")
def fetch_hdx_data(self, country: str = "vietnam"):
    """
    Fetch disaster history from HDX.
    """
    try:
        # Simulate HDX API call
        time.sleep(2)
        
        return {
            "status": "success",
            "data_type": "hdx",
            "country": country,
            "disasters_count": 50,
            "fetched_at": datetime.now().isoformat(),
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    "fetch-srtm-daily": {
        "task": "tasks.fetch_srtm_data",
        "schedule": 86400.0,  # Every 24 hours
        "args": ({"bounds": [102, 8, 110, 24]},),  # Vietnam bounds
    },
    "fetch-gpm-daily": {
        "task": "tasks.fetch_gpm_data",
        "schedule": 86400.0,
        "args": (
            {"bounds": [102, 8, 110, 24]},
            "2026-01-01",
            "2026-12-31",
        ),
    },
    "fetch-hdx-weekly": {
        "task": "tasks.fetch_hdx_data",
        "schedule": 604800.0,  # Every 7 days
        "args": ("vietnam",),
    },
    "cleanup-old-data-monthly": {
        "task": "tasks.cleanup_old_data",
        "schedule": 2592000.0,  # Every 30 days
        "args": (90,),
    },
}
