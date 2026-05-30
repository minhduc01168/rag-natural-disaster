from typing import Dict, Any, Optional
from app.slow_lane.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class WeatherAgent(BaseAgent):
    """
    Agent specialized in weather-related queries.
    """

    def __init__(self):
        super().__init__(
            name="WeatherAgent",
            description="Handles weather queries, forecasts, and alerts"
        )

    def can_handle(self, query: str) -> float:
        """Check if query is weather-related."""
        weather_keywords = [
            "thời tiết", "nhiệt độ", "mưa", "bão", "gió", "nắng",
            "weather", "temperature", "rain", "storm", "wind",
            "dự báo", "cảnh báo", "lũ", "lụt"
        ]
        query_lower = query.lower()
        matches = sum(1 for keyword in weather_keywords if keyword in query_lower)
        return min(matches * 0.3, 1.0)

    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process weather-related query."""
        try:
            # Mock weather response
            response = """
            Thời tiết hiện tại tại Hà Nội:
            - Nhiệt độ: 28°C
            - Độ ẩm: 75%
            - Gió: 12 km/h
            - Tình trạng: Nhiều mây
            
            Dự báo: Có thể mưa rào vào chiều tối.
            
            Khuyến nghị: Mang theo áo mưa khi ra ngoài.
            """

            return self._format_response(
                response=response.strip(),
                confidence=0.85,
                sources=["Meteostat API", "Dự báo thời tiết"]
            )

        except Exception as e:
            logger.error(f"WeatherAgent error: {e}")
            return self._format_response(
                response="Xin lỗi, tôi không thể lấy dữ liệu thời tiết lúc này.",
                confidence=0.3
            )


weather_agent = WeatherAgent()
