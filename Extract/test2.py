import requests
import json
from collections import defaultdict
from datetime import datetime
import asyncio

crypto=['CYBERUSDT','BTCUSDT']

data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']

async def scrap2(crypto, data):
    result = defaultdict(dict)
    for value in data:
        for item in crypto:
            if value['s'].startswith(item):
                result[value['b']] = {"HIGH": round(float(value['h']), 2), "LOW": round(float(value['l']), 2), "CURRENT": round(float(value['c']), 2)}
    formatted = "\n".join("{0} {1}".format(k, v)  for k,v in result.items())
    print(formatted)
    pass

async def scrap(crypto, data):
    result = defaultdict(dict)
    for i in crypto:
        data = requests.get(f"https://api.binance.com/api/v3/ticker?symbol={i}")
        response_data = json.loads(data.text)
        result[response_data['symbol']] = {"LAST": round(float(response_data['lastPrice']), 2), "OPENTIME": str(datetime.fromtimestamp(round(float(response_data['openTime'])/1000))), "CLOSETIME": str(datetime.fromtimestamp(round(float(response_data['closeTime'])/1000))), "COUNT": response_data['count'], "STATUS": str(data.status_code)}
        # print(data.status_code)
        # print(data.text)
    formatted = "\n".join("{0} {1}".format(k, v)  for k,v in result.items())
    print(formatted)
    # result = data.json()
    pass

async def show_params():
    result = defaultdict(dict)
    print((requests.get(f"https://api.binance.com/api/v3/ticker?symbol=BTCUSDT")).text)
    data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']
    for value in data:
        if value['s'].startswith("BTCDOWN"):
            result[value['b']] = {"HIGH": round(float(value['h']), 2), "LOW": round(float(value['l']), 2), "CURRENT": round(float(value['c']), 2)}
    print(result)

async def main(crypto, data):
    while True:
        task1 = asyncio.create_task(scrap(crypto, data))
        task2 = asyncio.create_task(scrap2(crypto, data))

        await asyncio.gather(task1, task2)
        await asyncio.sleep(5)

try:
    asyncio.run(main(crypto, data))
except KeyboardInterrupt:
    pass