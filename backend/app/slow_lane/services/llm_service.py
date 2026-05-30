from typing import Dict, Any, Optional, AsyncGenerator
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()


class LLMService:
    """
    Service for interacting with LLM APIs (Gemini/Groq).
    Supports Vietnamese language with fallback to mock responses.
    """

    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.groq_key = settings.GROQ_API_KEY
        self.initialized = False

    async def initialize(self):
        """Initialize LLM service."""
        try:
            if self.gemini_key or self.groq_key:
                self.initialized = True
                logger.info("LLM service initialized with API keys")
            else:
                self.initialized = True
                logger.warning("LLM service running in mock mode (no API keys)")
        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")

    async def generate_response(
        self,
        query: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate a response using LLM API.
        Falls back to mock if API unavailable.
        """
        try:
            if self.gemini_key:
                return await self._call_gemini(query, context, system_prompt)
            elif self.groq_key:
                return await self._call_groq(query, context, system_prompt)
            else:
                return self._mock_response(query, context)

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return self._mock_response(query, context)

    async def _call_gemini(self, query: str, context: Optional[str], system_prompt: Optional[str]) -> str:
        """Call Gemini API."""
        # Mock implementation - in production: use google.generativeai
        logger.info("Calling Gemini API")
        return self._mock_response(query, context)

    async def _call_groq(self, query: str, context: Optional[str], system_prompt: Optional[str]) -> str:
        """Call Groq API."""
        # Mock implementation - in production: use groq client
        logger.info("Calling Groq API")
        return self._mock_response(query, context)

    def _mock_response(self, query: str, context: Optional[str] = None) -> str:
        """Generate mock response when API is unavailable."""
        query_lower = query.lower()

        if any(word in query_lower for word in ["thời tiết", "mưa", "nắng", "bão"]):
            return """
            Dựa trên dữ liệu thời tiết hiện tại:
            
            Khu vực Hà Nội đang có thời tiết nhiều mây, nhiệt độ khoảng 28°C.
            Dự báo có thể mưa rào vào chiều tối.
            
            Bạn nên mang theo áo mưa và theo dõi bản tin thời tiết thường xuyên.
            """

        elif any(word in query_lower for word in ["sơ cấp cứu", "CPR", "cấp cứu"]):
            return """
            Về sơ cấp cứu cơ bản:
            
            1. Đảm bảo an toàn cho bản thân trước
            2. Gọi cấp cứu 115 ngay lập tức
            3. Thực hiện CPR nếu nạn nhân không thở:
               - Ép ngực 30 lần
               - Thổi ngạt 2 lần
               - Lặp lại cho đến khi cứu thương đến
            
            Lưu ý: Đây là hướng dẫn cơ bản. Hãy tham gia khóa học CPR để được đào tạo bài bản.
            """

        elif any(word in query_lower for word in ["lũ", "lụt", "ngập"]):
            return """
            Khi gặp lũ lụt:
            
            1. Di chuyển ngay đến nơi cao hơn
            2. Không đi qua vùng nước chảy xiết
            3. Tắt điện và gas để tránh cháy nổ
            4. Chuẩn bị đồ cấp cứu và nước uống
            5. Liên hệ cứu hộ nếu cần thiết
            
            Số điện thoại khẩn cấp:
            - Cấp cứu: 115
            - Cứu hỏa: 114
            - Cảnh sát: 113
            """

        else:
            return f"""
            Cảm ơn bạn đã đặt câu hỏi.
            
            Tôi là TerraBot, trợ lý AI của hệ thống cảnh báo thiên tai TerraAlert.
            
            Tôi có thể giúp bạn với:
            - Thông tin thời tiết và cảnh báo
            - Kiến thức phòng chống thiên tai
            - Kỹ năng sinh tồn và sơ cấp cứu
            - Thông tin địa lý và bản đồ
            
            Bạn có thể hỏi cụ thể hơn về chủ đề nào?
            """

    async def stream_response(
        self,
        query: str,
        context: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream response token by token.
        """
        response = await self.generate_response(query, context)
        
        # Simulate streaming by yielding chunks
        words = response.split()
        for i, word in enumerate(words):
            if i > 0:
                yield " "
            yield word


llm_service = LLMService()
