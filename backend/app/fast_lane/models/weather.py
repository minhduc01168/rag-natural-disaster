from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WeatherData(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    condition: str
    location_name: str
    latitude: float
    longitude: float
    timestamp: datetime
    rainfall: Optional[float] = 0.0


class WeatherResponse(BaseModel):
    status: str
    data: WeatherData
