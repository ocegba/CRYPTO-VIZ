import asyncio
import websockets
import datetime

async def on_message(message):
    print()
    print(str(datetime.datetime.now()) + ": ")
    print(message)

async def on_error(error):
    print("error", error)

async def on_close(close_msg):
    print("### closed ###" + close_msg)

async def streamKline(currency, interval, nifi_host, nifi_port):

    uri = f'wss://stream.binance.com:9443/ws/{currency}@kline_{interval}'
    async with websockets.connect(uri) as ws_binance:
        while True:
            try:
                message = await ws_binance.recv()
                await on_message(message)

                async with websockets.connect(f"ws://{nifi_host}:{nifi_port}/binance") as ws_nifi: #ListenWebSocket 
                    await ws_nifi.send(message)
                    print("Sent to NiFi")

            except websockets.exceptions.ConnectionClosedError as e:
                await on_close(str(e))
                break

            except Exception as e:
                await on_error(str(e))

async def main():
    currency = 'btcusdt'
    interval = '1m'
    nifi_host = "nifi"
    nifi_port = 6993

    await streamKline(currency, interval, nifi_host, nifi_port)

if __name__ == "__main__":
    asyncio.run(main())
