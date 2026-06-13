import json
from app.rag.agents.llm_generator import LLMGenerator

class RouterAgent:
    """
    Agent định tuyến câu hỏi của người dùng đến đúng bộ phận xử lý:
    1. KnowledgeBase (RAG): Câu hỏi về sơ cứu, kiến thức phòng chống thiên tai
    2. WeatherTool: Câu hỏi về thời tiết
    3. GeoTool: Câu hỏi về rủi ro địa lý, bản đồ, ngập lụt, sạt lở
    
    Sử dụng LLM để Semantic Routing và Trích xuất thực thể (Location).
    """
    def __init__(self, llm_generator: LLMGenerator = None):
        self.llm = llm_generator or LLMGenerator(mock=False)

    def route_query(self, query: str) -> dict:
        """
        Xác định đích đến của câu hỏi và trích xuất địa điểm.
        Trả về JSON dict có dạng:
        {
            "route": "weather" | "geo" | "knowledge",
            "location": "Tên địa phương" | null
        }
        """
        prompt = f"""Bạn là một hệ thống phân loại câu hỏi (Router) cho ứng dụng cảnh báo thiên tai.
Nhiệm vụ của bạn là đọc câu hỏi của người dùng và trả về một JSON HỢP LỆ (chỉ có JSON, không có text nào khác) với 2 trường:
- "route": Chọn 1 trong 3 giá trị:
  - "weather": Nếu người dùng hỏi về thời tiết, nhiệt độ, mưa, nắng, bão.
  - "geo": Nếu người dùng hỏi về rủi ro địa lý, sạt lở, ngập lụt tại một khu vực cụ thể, tọa độ.
  - "knowledge": Nếu người dùng hỏi về kiến thức chung, cách sơ cứu, định nghĩa thiên tai, biện pháp phòng tránh, hoặc không rõ ý định.
- "location": Trích xuất tên địa phương/tỉnh/thành phố mà người dùng nhắc đến. Nếu không có, hãy để là null.

Câu hỏi: "{query}"

JSON:"""
        try:
            # We bypass the context-generation logic of LLMGenerator and just use its model
            response = self.llm.model.generate_content(prompt)
            print(f"DEBUG LLM RAW: {response.text}")
            # Dọn dẹp markdown code block nếu có
            text = response.text.replace("```json", "").replace("```", "").strip()
            result = json.loads(text)
            
            # Đảm bảo fallback
            if result.get("route") not in ["weather", "geo", "knowledge"]:
                result["route"] = "knowledge"
                
            return result
        except Exception as e:
            # Fallback nếu LLM bị lỗi
            print(f"Router LLM Error: {e}")
            return {"route": "knowledge", "location": None}
