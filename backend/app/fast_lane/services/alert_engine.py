import yaml
from pathlib import Path
from typing import Dict, Any
from app.fast_lane.models.alert import AlertLevel, AlertResponse

# Load rules from YAML file
RULES_PATH = Path(__file__).parent.parent / "config" / "alert_rules.yaml"


def load_rules() -> Dict[str, Any]:
    """Load alert rules from YAML configuration file."""
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return _get_default_rules()


def _get_default_rules() -> Dict[str, Any]:
    """Return default rules if config file not found."""
    return {
        "green": {
            "name": "An toàn",
            "description": "Thời tiết bình thường",
            "temp_range": [15, 35],
            "humidity_range": [30, 80],
            "wind_speed_max": 30,
            "rainfall_max": 10,
            "recommendations": ["Thời tiết thuận lợi"],
        },
        "yellow": {
            "name": "Cảnh giác",
            "description": "Thời tiết bất thường",
            "temp_range": [10, 40],
            "humidity_range": [20, 90],
            "wind_speed_max": 60,
            "rainfall_max": 50,
            "recommendations": ["Hạn chế ra ngoài"],
        },
        "red": {
            "name": "Nguy hiểm",
            "description": "Thời tiết cực đoan",
            "temp_range": [-10, 50],
            "humidity_range": [0, 100],
            "wind_speed_max": 120,
            "rainfall_max": 200,
            "recommendations": ["Ở trong nhà"],
        },
    }


def classify_weather(
    temperature: float,
    humidity: float,
    wind_speed: float,
    rainfall: float = 0.0,
) -> AlertResponse:
    """
    Classify weather conditions into alert levels.
    
    Logic: Check from RED (highest) to GREEN (lowest).
    - RED: Any condition exceeds RED thresholds
    - YELLOW: Any condition exceeds GREEN thresholds (but not RED)
    - GREEN: All conditions within GREEN thresholds
    """
    rules = load_rules()
    
    red_rules = rules.get("red", {})
    yellow_rules = rules.get("yellow", {})
    green_rules = rules.get("green", {})
    
    # Check RED level first (highest priority)
    if _exceeds_level(temperature, humidity, wind_speed, rainfall, red_rules, yellow_rules):
        return _build_response(AlertLevel.RED, red_rules, temperature, humidity, wind_speed, rainfall)
    
    # Check YELLOW level (exceeds GREEN but not RED)
    if _exceeds_level(temperature, humidity, wind_speed, rainfall, yellow_rules, green_rules):
        return _build_response(AlertLevel.YELLOW, yellow_rules, temperature, humidity, wind_speed, rainfall)
    
    # Default to GREEN
    return _build_response(AlertLevel.GREEN, green_rules, temperature, humidity, wind_speed, rainfall)


def _exceeds_level(
    temp: float,
    humidity: float,
    wind_speed: float,
    rainfall: float,
    current_level_rules: Dict[str, Any],
    lower_level_rules: Dict[str, Any],
) -> bool:
    """
    Check if weather conditions exceed the lower level thresholds.
    Returns True if ANY metric is outside the lower level's acceptable range.
    """
    # Temperature check
    lower_temp_range = lower_level_rules.get("temp_range", [-100, 100])
    if temp < lower_temp_range[0] or temp > lower_temp_range[1]:
        return True
    
    # Humidity check
    lower_humidity_range = lower_level_rules.get("humidity_range", [0, 100])
    if humidity < lower_humidity_range[0] or humidity > lower_humidity_range[1]:
        return True
    
    # Wind speed check
    lower_wind_max = lower_level_rules.get("wind_speed_max", 999)
    if wind_speed > lower_wind_max:
        return True
    
    # Rainfall check
    lower_rainfall_max = lower_level_rules.get("rainfall_max", 999)
    if rainfall > lower_rainfall_max:
        return True
    
    return False


def _build_response(
    level: AlertLevel,
    rules: Dict[str, Any],
    temp: float,
    humidity: float,
    wind_speed: float,
    rainfall: float,
) -> AlertResponse:
    """Build alert response from rules and weather data."""
    return AlertResponse(
        level=level,
        name=rules.get("name", "Unknown"),
        description=rules.get("description", ""),
        recommendations=rules.get("recommendations", []),
        temperature=temp,
        humidity=humidity,
        wind_speed=wind_speed,
        rainfall=rainfall,
    )
