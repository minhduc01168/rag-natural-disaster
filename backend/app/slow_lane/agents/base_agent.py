from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all TerraBot agents.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.initialized = False

    async def initialize(self):
        """Initialize the agent."""
        self.initialized = True
        logger.info(f"Agent {self.name} initialized")

    @abstractmethod
    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user query and return a response.
        
        Returns:
            {
                "agent": str,
                "response": str,
                "confidence": float,
                "sources": list[str],
            }
        """
        pass

    def can_handle(self, query: str) -> float:
        """
        Return confidence score (0-1) for handling this query.
        Override in subclasses for specific routing.
        """
        return 0.5

    def _format_response(self, response: str, confidence: float = 0.8, sources: list = None) -> Dict[str, Any]:
        """Format agent response."""
        return {
            "agent": self.name,
            "response": response,
            "confidence": confidence,
            "sources": sources or [],
        }
