from typing import List

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from utils.logger import logger


class ConnectionManager:
    """
    Manages all active WebSocket connections.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept a new WebSocket connection.
        """
        await websocket.accept()

        if websocket not in self.active_connections:
            self.active_connections.append(websocket)

        logger.info(
            f"WebSocket connected | Active Connections: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove a disconnected WebSocket.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        logger.info(
            f"WebSocket disconnected | Active Connections: {len(self.active_connections)}"
        )

    async def send_json(
        self,
        websocket: WebSocket,
        data: dict,
    ) -> None:
        """
        Send JSON data to one client.
        """
        try:
            await websocket.send_json(data)
        except WebSocketDisconnect:
            self.disconnect(websocket)
        except Exception as e:
            logger.exception(f"Failed to send WebSocket message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, data: dict) -> None:
        """
        Broadcast JSON data to all connected clients.
        """
        disconnected = []

        for websocket in self.active_connections:
            try:
                await websocket.send_json(data)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(websocket)

    @property
    def connection_count(self) -> int:
        """
        Returns the number of active connections.
        """
        return len(self.active_connections)


manager = ConnectionManager()