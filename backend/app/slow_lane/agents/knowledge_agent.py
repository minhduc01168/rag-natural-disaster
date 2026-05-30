from typing import Dict, Any, Optional
from app.slow_lane.agents.base_agent import BaseAgent
from app.slow_lane.knowledge.document_loader import document_loader
import logging

logger = logging.getLogger(__name__)


class KnowledgeAgent(BaseAgent):
    """
    Agent specialized in disaster prevention knowledge queries.
    Uses RAG (Retrieval-Augmented Generation) with knowledge base.
    """

    def __init__(self):
        super().__init__(
            name="KnowledgeAgent",
            description="Handles disaster prevention and survival knowledge queries"
        )

    def can_handle(self, query: str) -> float:
        """Check if query is knowledge-related."""
        knowledge_keywords = [
            "sơ cấp cứu", "CPR", "cầm máu", "sinh tồn", "thức ăn", "nước",
            "phòng chống", "thiên tai", "bão", "lũ", "sạt lở", "động đất",
            "an toàn", "cấp cứu", "trú ẩn", "cứu hộ",
            "first aid", "survival", "disaster", "safety"
        ]
        query_lower = query.lower()
        matches = sum(1 for keyword in knowledge_keywords if keyword in query_lower)
        return min(matches * 0.3, 1.0)

    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process knowledge-related query using RAG."""
        try:
            # Search knowledge base
            relevant_docs = document_loader.search_documents(query)

            if relevant_docs:
                # Use the most relevant document
                doc = relevant_docs[0]
                response = f"**{doc['title']}**\n\n{doc['content'].strip()}"
                sources = [f"Knowledge Base: {doc['title']}"]
            else:
                # Fallback response
                response = """
                Tôi không tìm thấy thông tin cụ thể cho câu hỏi của bạn.
                
                Một số chủ đề tôi có thể giúp:
                - Sơ cấp cứu (CPR, cầm máu)
                - Xử lý thiên tai (lũ lụt, bão, sạt lở)
                - Kỹ năng sinh tồn (tìm nước, thức ăn)
                - Xây dựng nơi trú ẩn
                
                Bạn có thể hỏi cụ thể hơn về chủ đề nào?
                """
                sources = []

            return self._format_response(
                response=response.strip(),
                confidence=0.9 if relevant_docs else 0.5,
                sources=sources
            )

        except Exception as e:
            logger.error(f"KnowledgeAgent error: {e}")
            return self._format_response(
                response="Xin lỗi, tôi không thể truy vấn kiến thức lúc này.",
                confidence=0.3
            )


knowledge_agent = KnowledgeAgent()
