#!/usr/bin/env python
# python3 -m pip install websockets

import json
import asyncio
from websockets.server import serve

def getIpAddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddress = s.getsockname()[0]
    s.close()
    return ipaddress

ipaddress = getIpAddress()
port = 8765

async def echo(websocket):
    async for message in websocket:
        print("received from {}:{} : ".format(websocket.remote_address[0],websocket.remote_address[1]) + message)
        
        if '{' not in message:
            # if message is not json
            await websocket.send(message)
        else:
            # if message is json
            data = json.loads(message)
            answer = {}
            if(data['type'] == 'setParam'):
                answer['type'] = data['type']
                if(data['param1']<100 and data['param2']>1.2):
                    answer['valid'] = True
                    for key, val in data.items():
                        print("\t"+key+": ", val)
                else:
                    answer['valid'] = False
            else:
                answer['type'] = 'unknown'
                answer['valid'] = False
                
            await websocket.send(json.dumps(answer))


async def main():
    start_server = await serve(echo, "0.0.0.0", port)
    print("Server started")
    try:
        await asyncio.Future()  # Run forever until cancelled
    except asyncio.CancelledError:
        print("Server shutdown")
        start_server.close()  # Close the server
        await start_server.wait_closed()  # Wait until the server is closed

asyncio.run(main())
