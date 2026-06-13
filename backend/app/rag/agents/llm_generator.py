import os
import google.generativeai as genai

class LLMGenerator:
    """
    Sử dụng Google Gemini để tổng hợp thông tin (context) và sinh ra câu trả lời tự nhiên.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash", mock: bool = False):
        self.mock = mock
        if not self.mock:
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Cảnh báo: Không tìm thấy GEMINI_API_KEY trong environment variables.")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)

    def generate_answer(self, query: str, context: str) -> str:
        """
        Sinh câu trả lời dựa trên context.
        """
        if self.mock:
            return f"[MOCK_LLM_RESPONSE] Dựa vào context cung cấp, câu trả lời cho '{query}' là: {context}"

        prompt = f"""Bạn là một chuyên gia cứu hộ và phòng chống thiên tai (TerraBot).
Hãy trả lời câu hỏi của người dùng một cách chính xác, ngắn gọn và dễ hiểu, CHỈ DỰA VÀO phần Context được cung cấp bên dưới.
Nếu Context không chứa thông tin để trả lời, hãy nói rằng bạn không biết, tuyệt đối KHÔNG tự bịa ra thông tin.

Câu hỏi: {query}

Context:
{context}

Câu trả lời của bạn:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Đã xảy ra lỗi khi gọi LLM: {str(e)}"
