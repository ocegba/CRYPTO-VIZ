import requests
import json
from collections import defaultdict
from datetime import datetime
import asyncio

crypto=['CYBERUSDT','BTCUSDT'] #ajouter crypto ici

data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data'] #pour l'instant utilisé que sur scrap_price

async def scrap_price(crypto, data):
    result = defaultdict(dict)
    for value in data:
        for item in crypto:
            if value['s'].startswith(item):
                result[value['b']] = {"HIGH": round(float(value['h']), 2), "LOW": round(float(value['l']), 2), "CURRENT": round(float(value['c']), 2)}
    formatted = "\n".join("{0} {1}".format(k, v)  for k,v in result.items())
    print(formatted)
    pass
#OUTPUT UNFILTERED : 's': 'BTCDOWNUSDT', 'st': 'TRADING', 'b': 'BTCDOWN', 'q': 'USDT', 'ba': '', 'qa': '', 'i': '0.01000000', 'ts': '0.000001', 'an': 'BTCDOWN', 'qn': 'TetherUS', 'o': '0.009098', 'h': '0.009146', 'l': '0.008602', 'c': '0.008997', 'v': '84120759.730000', 'qv': '746979.88479539', 'y': 0, 'as': 84120759.73, 'pm': 'USDT', 'pn': 'USDT', 'cs': 0, 'tags': ['ETF'], 'pom': False, 'pomt': None, 'lc': False, 'g': False, 'sd': False, 'r': False, 'hd': False, 'rb': True, 'ks': False, 'etf': True

async def scrap_time(crypto, data):
    result = defaultdict(dict)
    for i in crypto:
        data = requests.get(f"https://api.binance.com/api/v3/ticker?symbol={i}")
        response_data = json.loads(data.text)
        result[response_data['symbol']] = {"LAST": round(float(response_data['lastPrice']), 2), "OPENTIME": str(datetime.fromtimestamp(round(float(response_data['openTime'])/1000))), "CLOSETIME": str(datetime.fromtimestamp(round(float(response_data['closeTime'])/1000))), "COUNT": response_data['count'], "STATUS": str(data.status_code)}
    formatted = "\n".join("{0} {1}".format(k, v)  for k,v in result.items())
    print(formatted)
    # result = data.json()
    pass
#OUTPUT UNFILTERED : "symbol":"BTCUSDT","priceChange":"136.80000000","priceChangePercent":"0.523","weightedAvgPrice":"26421.44010585","openPrice":"26165.88000000","highPrice":"26850.00000000","lowPrice":"26112.06000000","lastPrice":"26302.68000000","volume":"34284.63167000","quoteVolume":"905849342.22008690","openTime":1695766020000,"closeTime":1695852463885,"firstId":3220803882,"lastId":3221736941,"count":933060

def show_params():
    print((requests.get(f"https://api.binance.com/api/v3/ticker?symbol=BTCUSDT")).text)
    data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']
    for value in data:
        if value['s'].startswith("BTCDOWN"):
            print(value)
#SERT JUSTE A AVOIR LES OUTPUTS PLUS HAUT

async def main(crypto, data):
    while True:
        task1 = asyncio.create_task(scrap_time(crypto, data))
        task2 = asyncio.create_task(scrap_price(crypto, data))

        await asyncio.gather(task1, task2)
        await asyncio.sleep(5) #en secondes

try:
    asyncio.run(main(crypto, data))
except KeyboardInterrupt:
    pass