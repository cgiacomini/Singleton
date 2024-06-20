#!/usr/bin/env python
# python3 -m pip install websockets

import json
import asyncio
import argparse
import websockets

jsondata = {"type": "setParam", "param1": 30, "param2": 2.3}
jsonwrong = {"type": "setParam", "param1": 30, "param2": -2.3}
jsonunkn = {"type": "setData", "param1": 30, "param2": 2.3}

async def hello(address, port):
    uri = f"ws://{address}:{port}"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        message = await websocket.recv()
        print(f"Received from server: {message}")

        # send json valid data
        await websocket.send(json.dumps(jsondata))
        message = await websocket.recv()
        print(f"Received from server : {message}")
        
        # send json invalid data
        await websocket.send(json.dumps(jsonwrong))
        message = await websocket.recv()
        print(f"Received from server : {message}")
             
        # send json unknown data
        await websocket.send(json.dumps(jsonunkn))
        message = await websocket.recv()
        print(f"Received from server : {message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket client")
    parser.add_argument("--address", default="localhost", help="Server address")
    parser.add_argument("--port", type=int, default=8765, help="Server port")

    args = parser.parse_args()
    if not args.address and not args.port:
        print("No arguments provided.")
        parser.print_usage()
        exit(1)
    else:
        asyncio.run(hello(args.address, args.port))

