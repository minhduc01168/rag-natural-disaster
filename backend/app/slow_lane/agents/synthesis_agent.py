from typing import Dict, Any, Optional, List
from app.slow_lane.agents.base_agent import BaseAgent
from app.slow_lane.agents.weather_agent import weather_agent
from app.slow_lane.agents.geo_agent import geo_agent
from app.slow_lane.agents.knowledge_agent import knowledge_agent
import logging

logger = logging.getLogger(__name__)


class SynthesisAgent(BaseAgent):
    """
    Agent that combines insights from other agents to generate comprehensive responses.
    """

    def __init__(self):
        super().__init__(
            name="SynthesisAgent",
            description="Combines insights from multiple agents"
        )
        self.agents = [weather_agent, geo_agent, knowledge_agent]

    def can_handle(self, query: str) -> float:
        """Synthesis agent can handle any query by delegating."""
        return 0.5

    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process query by routing to appropriate agents and synthesizing results.
        """
        try:
            # Find the best agent for this query
            best_agent = None
            best_confidence = 0.0

            for agent in self.agents:
                confidence = agent.can_handle(query)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_agent = agent

            # If no strong match, use knowledge agent as default
            if best_agent is None or best_confidence < 0.3:
                best_agent = knowledge_agent

            # Get response from the best agent
            agent_response = await best_agent.process(query, context)

            # Format synthesis response
            response = agent_response.get("response", "")
            sources = agent_response.get("sources", [])
            confidence = agent_response.get("confidence", 0.5)

            return self._format_response(
                response=response,
                confidence=confidence,
                sources=sources
            )

        except Exception as e:
            logger.error(f"SynthesisAgent error: {e}")
            return self._format_response(
                response="Xin lỗi, tôi không thể xử lý câu hỏi lúc này. Vui lòng thử lại.",
                confidence=0.2
            )


synthesis_agent = SynthesisAgent()
