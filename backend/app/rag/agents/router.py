class RouterAgent:
    """
    Agent định tuyến câu hỏi của người dùng đến đúng bộ phận xử lý:
    1. KnowledgeBase (RAG): Câu hỏi về sơ cứu, kiến thức phòng chống thiên tai
    2. WeatherTool: Câu hỏi về thời tiết
    3. GeoTool: Câu hỏi về rủi ro địa lý
    """
    def __init__(self):
        # Các keyword đơn giản cho Router (thực tế có thể dùng LLM để phân loại - Semantic Routing)
        self.weather_keywords = ["thời tiết", "mưa", "nắng", "bão", "nhiệt độ"]
        self.geo_keywords = ["rủi ro", "ngập lụt", "sạt lở ở", "bản đồ", "tọa độ", "khu vực"]

    def route_query(self, query: str) -> str:
        """
        Xác định đích đến của câu hỏi.
        Trả về: 'weather', 'geo', hoặc 'knowledge'
        """
        query_lower = query.lower()
        
        # Check weather
        if any(kw in query_lower for kw in self.weather_keywords):
            return "weather"
            
        # Check geo
        if any(kw in query_lower for kw in self.geo_keywords):
            return "geo"
            
        # Default fallback to RAG Knowledge Base
        return "knowledge"
