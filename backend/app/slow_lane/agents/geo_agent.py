from typing import Dict, Any, Optional
from app.slow_lane.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class GeoAgent(BaseAgent):
    """
    Agent specialized in geographic/GIS queries.
    """

    def __init__(self):
        super().__init__(
            name="GeoAgent",
            description="Handles location, terrain, and GIS queries"
        )

    def can_handle(self, query: str) -> float:
        """Check if query is geography-related."""
        geo_keywords = [
            "địa điểm", "vị trí", "bản đồ", "cao độ", "địa hình",
            "tọa độ", "vĩ độ", "kinh độ", "sông", "núi", "rừng",
            "location", "map", "elevation", "terrain", "coordinates"
        ]
        query_lower = query.lower()
        matches = sum(1 for keyword in geo_keywords if keyword in query_lower)
        return min(matches * 0.3, 1.0)

    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process geography-related query."""
        try:
            # Mock geographic response
            response = """
            Thông tin địa lý cho khu vực Hà Nội:
            
            - Tọa độ: 21.0285°N, 105.8542°E
            - Cao độ trung bình: 10-20m so với mực nước biển
            - Địa hình: Đồng bằng châu thổ sông Hồng
            - Khu vực có nguy cơ lũ lụt: Các quận ven sông
            
            Cảnh báo: Khu vực ven sông có nguy cơ ngập lụt khi mưa lớn.
            """

            return self._format_response(
                response=response.strip(),
                confidence=0.8,
                sources=["PostGIS", "Dữ liệu địa hình"]
            )

        except Exception as e:
            logger.error(f"GeoAgent error: {e}")
            return self._format_response(
                response="Xin lỗi, tôi không thể truy vấn dữ liệu địa lý lúc này.",
                confidence=0.3
            )


geo_agent = GeoAgent()
