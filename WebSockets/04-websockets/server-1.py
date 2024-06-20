import asyncio
import websockets

# Create handler for each connection
async def handler(websocket, path):
    data = await websocket.recv()
    reply = f"Data received as: {data}!"
    await websocket.send(reply)

async def main():
    start_server = await websockets.serve(handler, "localhost", 8000)
    print("Server started")

    try:
        await asyncio.Future()  # Run forever until cancelled
    except asyncio.CancelledError:
        print("Server shutdown")
        start_server.close()  # Close the server
        await start_server.wait_closed()  # Wait until the server is closed

asyncio.run(main())