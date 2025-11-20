import asyncio
import websockets
import json


class WebSocketServer:
    """
    Websocket Server mit JSON-RPC 2.0 Protokoll

    Ermöglicht Remote Procedure Calls über den Websocket.
    Unterstützt sowohl synchrone als auch asynchrone Server-Methoden

    Attributes:
        host (str): Server hostname
        port (int): Server port
    """

    def __init__(self, host: str = "localhost", port: int = 3000) -> None:
        """
        Konstruktor für den Websocket Server
        :param host: Hostname auf dem der Server läuft, default="localhost"
        :param port: Port des Servers, default=3000
        """
        self.host = host
        self.port = port

    def add_two_numbers(self, a: int, b: int) -> int:
        """
        Addiert zwei Zahlen
        :param a: Erste Zahl
        :param b: Zweite Zahl
        :return: Summe von a und b
        """
        return a + b

    async def handle_request(self, websocket) -> None:
        """
        Verarbeitet eingehende WebSocket-Anfragen

        Empfängt Requests, führt die entsprechende Methode aus und sendet das Ergebnis zurück.

        :param websocket: Websocket-Verbindung zum Client

        :raises: Exception: Bei JSON-Parse-Fehlern oder Methoden-Ausführungsfehlern
        """
        async for message in websocket:
            try:
                # Parse JSON-RPC Request
                request = json.loads(message)
                method_name = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                # Prüfe ob Methode existiert
                if not hasattr(self, method_name):
                    response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Methode '{method_name}' nicht gefunden"
                        },
                        "id": request_id
                    }
                else:
                    # Führe Methode aus
                    method = getattr(self, method_name)

                    # Falls Methode async ist wird sie awaited
                    if asyncio.iscoroutinefunction(method):
                        result = await method(**params)
                    else:
                        result = method(**params)

                    response = {
                        "jsonrpc": "2.0",
                        "result": result,
                        "id": request_id
                    }

            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    },
                    "id": request.get("id") if 'request' in locals() else None
                }

            # Sende Antwort zurück
            await websocket.send(json.dumps(response))

    async def start(self) -> None:
        """
        Startet den Websocket Server und läuft bis er manuell beendet wird
        """
        print(f'Server läuft auf {self.host}:{self.port}')
        async with websockets.serve(self.handle_request, self.host, self.port):
            await asyncio.Future()


if __name__ == '__main__':
    server = WebSocketServer()
    asyncio.run(server.start())
