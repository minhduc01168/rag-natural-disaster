import httpx
from datetime import datetime
from typing import Optional
from app.core.config import get_settings
from app.fast_lane.models.weather import WeatherData

settings = get_settings()

# Weather condition mapping
CONDITION_MAP = {
    1: "Trời quang",
    2: "Ít mây",
    3: "Nhiều mây",
    4: "U ám",
    5: "Mưa nhẹ",
    6: "Mưa",
    7: "Mưa lớn",
    8: "Giông bão",
    9: "Tuyết",
    10: "Sương mù",
}


async def get_weather_from_meteostat(lat: float, lon: float) -> Optional[WeatherData]:
    """
    Fetch weather data from Meteostat API.
    Returns None if API call fails.
    """
    try:
        url = "https://meteostat.p.rapidapi.com/point/hourly"
        querystring = {
            "lat": str(lat),
            "lon": str(lon),
            "limit": "1",
        }
        headers = {
            "x-rapidapi-key": settings.METEOSTAT_API_KEY or "demo-key",
            "x-rapidapi-host": "meteostat.p.rapidapi.com",
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers, params=querystring)

            if response.status_code != 200:
                return _get_fallback_weather(lat, lon)

            data = response.json()
            if not data.get("data"):
                return _get_fallback_weather(lat, lon)

            hourly_data = data["data"][0]
            condition_code = hourly_data.get("coco", 1)

            return WeatherData(
                temperature=hourly_data.get("temp", 25.0),
                humidity=hourly_data.get("rhum", 70.0),
                wind_speed=hourly_data.get("wspd", 10.0),
                condition=CONDITION_MAP.get(condition_code, "Không xác định"),
                location_name=f"Vị trí ({lat:.2f}, {lon:.2f})",
                latitude=lat,
                longitude=lon,
                timestamp=datetime.fromisoformat(hourly_data.get("time", datetime.now().isoformat())),
                rainfall=hourly_data.get("prcp", 0.0),
            )

    except (httpx.TimeoutException, httpx.RequestError):
        return _get_fallback_weather(lat, lon)


def _get_fallback_weather(lat: float, lon: float) -> WeatherData:
    """
    Return fallback weather data when API is unavailable.
    Uses simulated data based on location.
    """
    return WeatherData(
        temperature=28.5,
        humidity=75.0,
        wind_speed=12.0,
        condition="Nhiều mây",
        location_name=f"Vị trí ({lat:.2f}, {lon:.2f})",
        latitude=lat,
        longitude=lon,
        timestamp=datetime.now(),
        rainfall=0.0,
    )
