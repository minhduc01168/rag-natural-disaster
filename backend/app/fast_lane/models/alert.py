from pydantic import BaseModel
from typing import List
from enum import Enum


class AlertLevel(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class AlertResponse(BaseModel):
    level: AlertLevel
    name: str
    description: str
    recommendations: List[str]
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float
