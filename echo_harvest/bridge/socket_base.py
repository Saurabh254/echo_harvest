from .event_handler import SocketEventHandler
from echo_harvest.helpers.logger import logging as logger
import json
import asyncio
from websockets.server import serve


async def echo(websocket):
    async for message in websocket:
        data = json.dumps({"type": "status"})
        handler = SocketEventHandler(data)
        await websocket.send(handler.generate_response())
        logger.info("SOCKET::SERVER:CLIENT_RESPONSE: Sent status response")


async def main():
    async with serve(echo, "localhost", 6565):
        logger.info("SOCKET::SERVER:STARTED: Server started and listening")
        await asyncio.Future()
