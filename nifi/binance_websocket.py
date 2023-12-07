import asyncio
import websockets
import datetime

async def on_message(message):
    print()
    print(str(datetime.datetime.now()) + ": ")
    print(message)

async def on_error(error):
    print(error)

async def on_close(close_msg):
    print("### closed ###" + close_msg)

async def streamKline(currency, interval):
    uri = f'wss://stream.binance.com:9443/ws/{currency}@kline_{interval}'
    async with websockets.connect(uri) as ws:
        while True:
            try:
                message = await ws.recv()
                await on_message(message)
            except websockets.exceptions.ConnectionClosedError as e:
                await on_close(str(e))
                break
            except Exception as e:
                await on_error(str(e))

async def produce(message: str, host:str, port:int):
    async with websockets.connect(f"ws://{host}:{port}/binance") as ws:
        print(message)
        await ws.send(message)
        print("=============================================")
        await ws.recv()

async def main():
    currency = 'btcusdt'
    interval = '1m'

    await streamKline(currency, interval)

if __name__ == "__main__":
    asyncio.run(main())
