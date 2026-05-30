from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from datetime import datetime
import json


class NotificationManager:
    """Manages WebSocket connections and sends notifications."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific client."""
        await websocket.send_json(message)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def send_alert(self, alert_data: Dict[str, Any]):
        """Send an alert notification to all connected clients."""
        notification = {
            "type": "alert",
            "data": alert_data,
            "timestamp": datetime.now().isoformat(),
        }
        await self.broadcast(notification)
    
    @property
    def connection_count(self) -> int:
        return len(self.active_connections)


# Global notification manager
notification_manager = NotificationManager()
