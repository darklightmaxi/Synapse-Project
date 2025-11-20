import asyncio
import websockets
import json
from typing import Any


class WebSocketClient:
    """
    Websocket Client für JSON-RPC 2.0 Aufrufe

    Ermöglicht asynchrone Aufrufe von Server Funktionen über WebSocket
    """
    def __init__(self, uri: str = "ws://localhost:3000") -> None:
        """
        Konstruktor des Websocket Clients
        :param uri: Websocket URI des Servers, default="ws://localhost:3000"
        """
        self.uri = uri
        self.websocket = None
        self.request_id = 0

    async def connect(self) -> None:
        """
        Verbindet mit dem WebSocket Server

        :raises: WebsocketException bei Verbindungsfehlern
        """
        self.websocket = await websockets.connect(self.uri)
        print(f"Verbunden mit {self.uri}")

    async def disconnect(self) -> None:
        """
        Trennt die Verbindung zum Server und schließt die Websocket-Verbindung sauber
        :return:
        """
        if self.websocket:
            await self.websocket.close()
            print("Verbindung getrennt")

    async def call(self, method: str, **params) -> Any:
        """
        Ruft eine Remote-Methode auf dem Server auf

        Args:
            method: Name der Server-Methode
            **params: Parameter für die Methode als kwargs

        Returns:
            Das Ergebnis der Methode

        :raises:
            ConnectionError: Wenn keine Verbindung besteht
            Exception: Bei Server-Fehlern oder Netzwerkproblemen
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

    async def __aenter__(self) -> 'WebSocketClient':
        """
        Context Manager Entry Point

        Returns:
            self: Die Client Instanz
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context Manager Exit Point

        :arg exc_type: Exception Typ (falls vorhanden)
        :arg exc_val: Exception Wert (falls vorhanden)
        :arg exc_tb: Exception Traceback (falls vorhanden)
        """
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
    except Exception as e:
        print(f"Fehler: WS-Server konnte nicht verbunden werden - {e}")
        print("Überprüfe ob der Server läuft")


if __name__ == "__main__":
    asyncio.run(main())
