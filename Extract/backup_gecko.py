import requests
import json
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

crypto = [
    'CYBER',
    'BTC',
    'ETH',
    'LTC',
    'XRP',
    'BCH',
    'ADA',
    'DOT',
    'LINK',
    'XLM',
    'EOS',
    'BNB',
    'TRX',
    'XTZ',
    'XMR',
    'VET',
    'DOGE',
    'DASH',
    'ZEC',
    'UNI',
    'AAVE',
    'SOL',
    'ATOM',
    'MKR',
    'COMP',
    'THETA',
    'FIL',
    'BTT',
    'MANA',
    'ENJ',
    'SNX',
    'YFI',
    'CHZ',
    'BAT',
    'CRO',
    'NEO'
]  # Add more as needed

def scrap_price(crypto):
    data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']
    result = defaultdict(dict)
    for value in data:
        for item in crypto:
            if value['s'].startswith(item):
                result[value['b']] = {"HIGH": round(float(value['h']), 2), "LOW": round(float(value['l']), 2), "CURRENT": round(float(value['c']), 2)}
    formatted = "\n".join("{0} {1}".format(k, v) for k, v in result.items())
    print("scrap_price: " + formatted)
#OUTPUT UNFILTERED : 's': 'BTCDOWNUSDT', 'st': 'TRADING', 'b': 'BTCDOWN', 'q': 'USDT', 'ba': '', 'qa': '', 'i': '0.01000000', 'ts': '0.000001', 'an': 'BTCDOWN', 'qn': 'TetherUS', 'o': '0.009098', 'h': '0.009146', 'l': '0.008602', 'c': '0.008997', 'v': '84120759.730000', 'qv': '746979.88479539', 'y': 0, 'as': 84120759.73, 'pm': 'USDT', 'pn': 'USDT', 'cs': 0, 'tags': ['ETF'], 'pom': False, 'pomt': None, 'lc': False, 'g': False, 'sd': False, 'r': False, 'hd': False, 'rb': True, 'ks': False, 'etf': True

def scrap_time(crypto):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()

    result = defaultdict(dict)

    for symbol in crypto:
        for item in data:
            if item['symbol'].startswith(symbol):
                result[symbol] = {
                    "LAST": round(float(item['lastPrice']), 2),
                    "OPENTIME": str(datetime.fromtimestamp(round(float(item['openTime']) / 1000))),
                    "CLOSETIME": str(datetime.fromtimestamp(round(float(item['closeTime']) / 1000))),
                    "COUNT": item['count'],
                    "VOLUME": float(item['volume']),
                    "HIGH": float(item['highPrice']),
                    "LOW": float(item['lowPrice']),
                    "CURRENT": float(item['lastPrice']),
                    "STATUS": str(response.status_code)
                }
    formatted = "\n".join(f"{k} {v}" for k, v in result.items())
    print("scrap_time: " + formatted)
#OUTPUT UNFILTERED : "symbol":"BTCUSDT","priceChange":"136.80000000","priceChangePercent":"0.523","weightedAvgPrice":"26421.44010585","openPrice":"26165.88000000","highPrice":"26850.00000000","lowPrice":"26112.06000000","lastPrice":"26302.68000000","volume":"34284.63167000","quoteVolume":"905849342.22008690","openTime":1695766020000,"closeTime":1695852463885,"firstId":3220803882,"lastId":3221736941,"count":933060

def show_params():
    print((requests.get(f"https://api.binance.com/api/v3/ticker?symbol=BTCUSDT")).text)
    data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']
    for value in data:
        if value['s'].startswith("BTCDOWN"):
            print(value)
    print((requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")).text)
#SERT JUSTE A AVOIR LES OUTPUTS PLUS HAUT

def get_crypto_id_by_symbol(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for coin_info in data:
            if coin_info['symbol'].lower() == symbol.lower():
                return coin_info['id']
        return None
    else:
        return None

def get_crypto_data_by_symbol(symbol):
    coin_id = get_crypto_id_by_symbol(symbol)

    if coin_id:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            circulating_supply = data.get('market_data', {}).get('circulating_supply')
            max_supply = data.get('market_data', {}).get('total_supply')
            market_cap = data.get('market_data', {}).get('market_cap', {}).get('usd')
            ath = data.get('market_data', {}).get('ath', {}).get('usd')
            ath_date = data.get('market_data', {}).get('ath_date', {}).get('usd')
            last_updated = data.get('last_updated')

            return {
                "Coin" : symbol,
                "Circulating Supply": circulating_supply,
                "Max Supply": max_supply,
                "Market Cap (USD)": market_cap,
                "All-Time High (USD)": ath,
                "All-Time High Date": ath_date,
                "Last Updated": last_updated
            }
        else:
            return None
    else:
        return None

def get_gecko_data(symbol):
    crypto_data = get_crypto_data_by_symbol(symbol)
    if crypto_data is not None:
        for key, value in crypto_data.items():
            print(f"{key}: {value}")
    else:
        print("get_geck_data Unable to retrieve data for " + symbol)

def main(crypto):
    with ThreadPoolExecutor() as executor:
        futures = []
        for item in crypto:
            futures.append(executor.submit(scrap_price, [item]))
            futures.append(executor.submit(scrap_time, [item]))
            futures.append(executor.submit(get_gecko_data, item))
        
        for future in futures:
            future.result()
    time.sleep(5)  # Sleep for 5 seconds

if __name__ == "__main__":
    try:
        while True:
            main(crypto)
    except KeyboardInterrupt:
        pass