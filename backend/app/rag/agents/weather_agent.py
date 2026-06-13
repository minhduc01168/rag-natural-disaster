from app.rag.agents.llm_generator import LLMGenerator
from app.rag.tools.weather import WeatherTool

class WeatherAgent:
    """
    Sub-Agent chuyên biệt cho chức năng Thời tiết.
    - Nhận query và location từ Master Agent
    - Tự gọi WeatherTool lấy dữ liệu thực tế
    - Dùng LLM tổng hợp, phân tích, và dịch kết quả sang Tiếng Việt mượt mà.
    """
    def __init__(self, llm_generator: LLMGenerator = None, mock_tool: bool = False):
        self.llm = llm_generator or LLMGenerator(mock=False)
        self.weather_tool = WeatherTool(mock=mock_tool)
        
    def process(self, query: str, location: str) -> dict:
        """
        Xử lý truy vấn thời tiết.
        """
        target_location = location if location else "Hà Nội"
        
        # 1. Gọi Tool để lấy raw data (JSON)
        weather_data = self.weather_tool.get_weather(target_location)
        
        # 2. Xây dựng Context khô khan
        context = (
            f"Thông tin thời tiết tại {target_location}:\n"
            f"- Nhiệt độ: {weather_data.get('temperature', 'N/A')}\n"
            f"- Tình trạng: {weather_data.get('condition', 'N/A')}\n"
            f"- Tốc độ gió: {weather_data.get('wind_speed', 'N/A')}\n"
            f"- Độ ẩm: {weather_data.get('humidity', 'N/A')}"
        )
        
        # 3. Dùng LLM để phân tích và dịch ngữ cảnh
        prompt = f"""Bạn là một chuyên gia khí tượng học bằng tiếng Việt.
Dựa vào dữ liệu thời tiết thực tế dưới đây (có thể chứa tiếng Anh), hãy trả lời câu hỏi của người dùng bằng tiếng Việt một cách tự nhiên, chuyên nghiệp.

Dữ liệu (Context):
{context}

Câu hỏi của người dùng: "{query}"

Lưu ý:
- Dịch mượt mà tình trạng thời tiết (ví dụ: Partly Cloudy -> Trời có mây rải rác, Rain -> Có mưa, Clear -> Trời quang).
- Nhấn mạnh những yếu tố thời tiết cực đoan nếu có.
- Trả lời ngắn gọn, súc tích.

Câu trả lời:"""
        
        try:
            response = self.llm.model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            print(f"WeatherAgent LLM Error: {e}")
            answer = f"Thời tiết tại {target_location} hôm nay: Nhiệt độ {weather_data.get('temperature')}, {weather_data.get('condition')}."

        return {
            "answer": answer,
            "sources": ["[Dịch vụ Thời tiết Thực tế (wttr.in)](https://wttr.in)"] if not self.weather_tool.mock else ["Mock Weather API"]
        }
