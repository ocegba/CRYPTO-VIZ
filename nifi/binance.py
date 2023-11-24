import asyncio
import websockets

async def produce(message: str, host:str, port:int):
    async with websockets.connect(f"ws://{host}:{port}/binance") as ws:
        print(message)
        await ws.send(message)
        print("=============================================")
        await ws.recv()

loop = asyncio.get_event_loop()
loop.run_until_complete(produce(message='{"msg: "lol"}', host="nifi", port=6890))