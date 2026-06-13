from fastapi import APIRouter, HTTPException
import httpx
import time
from typing import Dict, Any

router = APIRouter()

# In-memory cache: {(lat, lon): (timestamp, data)}
WEATHER_CACHE: Dict[str, tuple[float, dict]] = {}
CACHE_TTL_SECONDS = 300  # 5 minutes

def get_weather_description(wmo_code: int) -> str:
    """Map WMO weather code to Vietnamese description."""
    wmo_mapping = {
        0: "Trời trong, không mây",
        1: "Trời quang mây tạnh",
        2: "Nhiều mây",
        3: "Âm u",
        45: "Sương mù",
        48: "Sương mù lạnh",
        51: "Mưa phùn nhẹ",
        53: "Mưa phùn vừa",
        55: "Mưa phùn dày đặc",
        61: "Mưa rào nhẹ",
        63: "Mưa rào vừa",
        65: "Mưa rào to",
        71: "Tuyết rơi nhẹ",
        80: "Mưa rào thoáng qua",
        81: "Mưa rào mạnh",
        82: "Mưa rào dữ dội",
        95: "Sấm chớp",
        96: "Sấm chớp kèm mưa đá nhẹ",
        99: "Sấm chớp kèm mưa đá mạnh"
    }
    return wmo_mapping.get(wmo_code, f"Không xác định (Code: {wmo_code})")

def generate_alert(rainfall: float, wind_speed: float) -> dict:
    """Generate simple rule-based alert based on weather metrics."""
    if rainfall > 50 or wind_speed > 60:
        return {
            "level": "red",
            "name": "Nguy hiểm",
            "description": "Thời tiết rất xấu, có nguy cơ ngập lụt hoặc gió giật mạnh.",
            "recommendations": ["Ở trong nhà", "Chuẩn bị đèn pin", "Sẵn sàng sơ tán nếu có lệnh"]
        }
    elif rainfall > 15 or wind_speed > 30:
        return {
            "level": "yellow",
            "name": "Cảnh giác",
            "description": "Mưa lớn hoặc gió mạnh, hạn chế ra ngoài.",
            "recommendations": ["Mang áo mưa", "Tránh khu vực nhiều cây to", "Theo dõi tin tức"]
        }
    else:
        return {
            "level": "green",
            "name": "An toàn",
            "description": "Thời tiết bình thường, không có nguy hiểm.",
            "recommendations": ["Hoạt động bình thường"]
        }

@router.get("/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
    cache_key = f"{lat},{lon}"
    current_time = time.time()
    
    # Check cache
    if cache_key in WEATHER_CACHE:
        timestamp, cached_data = WEATHER_CACHE[cache_key]
        if current_time - timestamp < CACHE_TTL_SECONDS:
            return cached_data

    # Fetch from Open-Meteo
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,weather_code"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            rainfall = current.get("precipitation", 0)
            wind_speed = current.get("wind_speed_10m", 0)
            
            weather_data = {
                "temperature": current.get("temperature_2m", 0),
                "humidity": current.get("relative_humidity_2m", 0),
                "wind_speed": wind_speed,
                "condition": get_weather_description(current.get("weather_code", 0)),
                "location_name": f"Vị trí ({lat}, {lon})",
                "rainfall": rainfall
            }
            
            alert_data = generate_alert(rainfall, wind_speed)
            
            result = {
                "status": "success",
                "data": weather_data,
                "alert": alert_data,
                "cached": False
            }
            
            # Save to cache
            WEATHER_CACHE[cache_key] = (current_time, result)
            return result
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather from Open-Meteo: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
