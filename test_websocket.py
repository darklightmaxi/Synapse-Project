"""
Test Suite für WebSocket RPC System
"""

import asyncio
import pytest
from websocket_server import WebSocketServer
from websocket_client import WebSocketClient


# ========================================
# Unit Tests für Server-Funktionen
# ========================================

class TestServerFunctions:
    """Unit Tests für einzelne Server-Funktionen"""
    
    def test_add_two_numbers_positive(self):
        """Test Addition mit positiven Zahlen"""
        server = WebSocketServer()
        result = server.add_two_numbers(5, 3)
        assert result == 8
    
    def test_add_two_numbers_negative(self):
        """Test Addition mit negativen Zahlen"""
        server = WebSocketServer()
        result = server.add_two_numbers(-5, -3)
        assert result == -8
    
    def test_add_two_numbers_mixed(self):
        """Test Addition mit gemischten Vorzeichen"""
        server = WebSocketServer()
        result = server.add_two_numbers(10, -3)
        assert result == 7
    
    def test_add_two_numbers_zero(self):
        """Test Addition mit Null"""
        server = WebSocketServer()
        result = server.add_two_numbers(0, 5)
        assert result == 5
    
    def test_add_two_numbers_large(self):
        """Test mit sehr großen Zahlen"""
        server = WebSocketServer()
        result = server.add_two_numbers(999999999, 1)
        assert result == 1000000000


# ========================================
# Integration Tests (benötigen laufenden Server)
# ========================================

@pytest.mark.asyncio
async def test_client_server_basic():
    """Test grundlegende Client-Server Kommunikation"""
    # Starte Server
    server = WebSocketServer(host="localhost", port=3099)
    server_task = asyncio.create_task(server.start())
    
    # Warte bis Server läuft
    await asyncio.sleep(0.1)
    
    try:
        # Teste Client-Aufruf
        async with WebSocketClient(uri="ws://localhost:3099") as client:
            result = await client.call("add_two_numbers", a=5, b=3)
            assert result == 8
    finally:
        # Cleanup
        server_task.cancel()
        await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_client_server_negative_numbers():
    """Test mit negativen Zahlen"""
    server = WebSocketServer(host="localhost", port=3098)
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(0.1)
    
    try:
        async with WebSocketClient(uri="ws://localhost:3098") as client:
            result = await client.call("add_two_numbers", a=-10, b=5)
            assert result == -5
    finally:
        server_task.cancel()
        await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_client_multiple_calls():
    """Test mehrere aufeinanderfolgende Aufrufe"""
    server = WebSocketServer(host="localhost", port=3097)
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(0.1)
    
    try:
        async with WebSocketClient(uri="ws://localhost:3097") as client:
            result1 = await client.call("add_two_numbers", a=1, b=2)
            result2 = await client.call("add_two_numbers", a=10, b=20)
            result3 = await client.call("add_two_numbers", a=100, b=200)
            
            assert result1 == 3
            assert result2 == 30
            assert result3 == 300
    finally:
        server_task.cancel()
        await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_invalid_method():
    """Test Aufruf einer nicht existierenden Methode"""
    server = WebSocketServer(host="localhost", port=3096)
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(0.1)
    
    try:
        async with WebSocketClient(uri="ws://localhost:3096") as client:
            with pytest.raises(Exception) as exc_info:
                await client.call("non_existent_method", a=5, b=3)
            
            assert "nicht gefunden" in str(exc_info.value)
    finally:
        server_task.cancel()
        await asyncio.sleep(0.1)


# ========================================
# Error Handling Tests
# ========================================

@pytest.mark.asyncio
async def test_call_without_connection():
    """Test Aufruf ohne aktive Verbindung"""
    client = WebSocketClient()
    
    with pytest.raises(ConnectionError):
        await client.call("add_two_numbers", a=5, b=3)


@pytest.mark.asyncio
async def test_connection_refused():
    """Test Verbindungsfehler wenn Server nicht läuft"""
    client = WebSocketClient(uri="ws://localhost:9999")
    
    with pytest.raises(Exception):  # Kann verschiedene Exception-Typen sein
        await client.connect()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
