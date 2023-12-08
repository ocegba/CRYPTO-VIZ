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
    async with websockets.connect(uri) as ws_nifi:
        print("hello", uri)
        while True:
            try:
                message = await ws_nifi.recv()
                await on_message(message)
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", nifi_host, nifi_port)
                async with websockets.connect(f"wss://{nifi_host}:{nifi_port}/binance") as ws_nifi: #ListenWebSocket 
                    print("--------------------------------------------------------------------------------------------------------------------------", nifi_host, nifi_port)
                    await ws_nifi.send("hello", message)
                    print("Sent to NiFi")

            except websockets.exceptions.ConnectionClosedError as e:
                await on_close(str(e))
                print('on close')
                break
            except Exception as e:
                print(nifi_host, "nifi_host")
                await on_error(str(e))
                print('on error')

async def produce(message: str, host:str, port:str):
    async with websockets.connect(f"ws://{host}:{port}/binance") as ws:
        print(message)
        await ws.send(message)
        print("===================================================================================================================================")
        await ws.recv()

async def main():
    currency = 'btcusdt'
    interval = '1m'
    nifi_host = "nifi"
    nifi_port = 6993

    await streamKline(currency, interval, nifi_host, nifi_port)

if __name__ == "__main__":
    asyncio.run(main())
