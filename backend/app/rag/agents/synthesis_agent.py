from app.rag.agents.router import RouterAgent
from app.rag.agents.knowledge_agent import KnowledgeAgent
from app.rag.agents.llm_generator import LLMGenerator
from app.rag.tools.weather import WeatherTool
from app.rag.tools.geo import GeoTool

class SynthesisAgent:
    """
    Master Orchestrator:
    1. Nhận query từ User
    2. Hỏi RouterAgent xem query thuộc loại nào
    3. Gọi Tool hoặc KnowledgeAgent tương ứng
    4. Tổng hợp (Synthesize) câu trả lời cuối cùng để trả về
    """
    def __init__(self, knowledge_agent: KnowledgeAgent = None, llm_mock: bool = True):
        self.router = RouterAgent()
        self.knowledge_agent = knowledge_agent or KnowledgeAgent()
        self.llm = LLMGenerator(mock=llm_mock)
        self.weather_tool = WeatherTool(mock=True)
        self.geo_tool = GeoTool(mock=True)

    def process_query(self, query: str) -> dict:
        """
        Xử lý truy vấn end-to-end.
        """
        # 1. Routing
        route = self.router.route_query(query)

        # 2. Xử lý dựa trên Route
        if route == "weather":
            # Trong thực tế, có thể dùng NLP để extract location từ query
            location = "Hà Nội" 
            weather_data = self.weather_tool.get_weather(location)
            context = f"Thời tiết tại {location}: Nhiệt độ {weather_data['temperature']}, {weather_data['condition']}. Gió: {weather_data['wind_speed']}."
            sources = ["OpenWeatherMap API"]
            
        elif route == "geo":
            location = "Lào Cai"
            geo_data = self.geo_tool.check_risk_zone(location)
            safe_zones = ", ".join(geo_data['safe_zones_nearby'])
            context = f"Cảnh báo: Khu vực {location} có mức rủi ro {geo_data['risk_level']} về {geo_data['disaster_type']}. Nơi an toàn gần nhất: {safe_zones}."
            sources = ["Geo Susceptibility Map API"]
            
        else: # "knowledge"
            result = self.knowledge_agent.answer_query(query)
            context = result["answer"] # Use the raw context retrieved by knowledge agent
            sources = result["sources"]

        # 3. Sinh câu trả lời tự nhiên bằng LLM
        final_answer = self.llm.generate_answer(query, context)

        # 4. Trả về format chuẩn
        return {
            "query": query,
            "route_taken": route,
            "answer": final_answer,
            "sources": sources
        }
