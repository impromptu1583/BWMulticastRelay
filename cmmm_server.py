#!/usr/bin/env python

import asyncio, websockets, json, logging

CONNECTIONS = set()

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)

class LoggerAdapter(logging.LoggerAdapter):
    """Add connection ID and client IP address to websockets logs."""
    def process(self, msg, kwargs):
        try:
            websocket = kwargs["extra"]["websocket"]
        except KeyError:
            return msg, kwargs
        return f"{websocket.id} {msg}", kwargs


async def broadcast_ip_list():
    ip_list = list(map(lambda ws:ws.remote_address[0],CONNECTIONS))
    websockets.broadcast(CONNECTIONS,json.dumps(ip_list))

async def handler(websocket):
    CONNECTIONS.add(websocket)
    await broadcast_ip_list()
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)
        await broadcast_ip_list()
        
async def main():
    async with websockets.serve(
        handler,
        None,
        8001,
        logger=LoggerAdapter(logging.getLogger("websockets.server"), None),
        ):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())