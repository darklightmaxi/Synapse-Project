import asyncio
import websockets
import json
from typing import Any


class WebSocketClient:
    def __init__(self, uri: str = "ws://localhost:3000"):
        self.uri = uri
        self.websocket = None
        self.request_id = 0

    async def connect(self):
        """Verbindet mit dem WebSocket Server"""
        self.websocket = await websockets.connect(self.uri)
        print(f"Verbunden mit {self.uri}")

    async def disconnect(self):
        """Trennt die Verbindung"""
        if self.websocket:
            await self.websocket.close()
            print("Verbindung getrennt")

    async def call(self, method: str, **params) -> Any:
        """
        Ruft eine Remote-Methode auf

        Args:
            method: Name der Methode
            **params: Parameter für die Methode

        Returns:
            Das Ergebnis der Methode
        """
        if not self.websocket:
            raise ConnectionError("Keine Verbindung zum Websocket")

        # Erstelle Request
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.request_id
        }

        # Sende Request
        await self.websocket.send(json.dumps(request))

        # Warte auf Antwort
        response_text = await self.websocket.recv()
        response = json.loads(response_text)

        # Prüfe auf Fehler
        if "error" in response:
            raise Exception(f"Server Error: {response['error']['message']}")

        return response.get("result")

    async def __aenter__(self):
        """Context Manager Support"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context Manager Support"""
        await self.disconnect()


async def main():
    try:
        async with WebSocketClient() as client:
            result = await client.call("add_two_numbers", a=5, b=3)
            print(f"5 + 3 = {result}")

        async with WebSocketClient() as client:
            result = await client.call("add_two_numbers", a=25, b=-17)
            print(f'25 + (-17) = {result}')
            result = await client.call("add_two_numbers", a=225, b=-17)
            print(f'225 + (-17) = {result}')
    except:
        print("WS-Server konnte nicht verbunden werden, überprüfe ob er läuft")


if __name__ == "__main__":
    asyncio.run(main())
