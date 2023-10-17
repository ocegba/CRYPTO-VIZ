import requests
import json
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

crypto = {
    'Bitcoin': 'BTCUSDT',
    'Ethereum': 'ETHUSDT',
    'Binance Coin': 'BNBUSDT',
    'Cardano': 'ADAUSDT',
    'Solana': 'SOLUSDT',
    'XRP': 'XRPUSDT',
    'Polkadot': 'DOTUSDT',
    'Dogecoin': 'DOGEUSDT',
    'Avalanche': 'AVAXUSDT',
    'Chainlink': 'LINKUSDT',
    'Litecoin': 'LTCUSDT',
    'Bitcoin Cash': 'BCHUSDT',
    'Cosmos': 'ATOMUSDT',
    'VeChain': 'VETUSDT',
    'Filecoin': 'FILUSDT',
    'Ethereum Classic': 'ETCUSDT',
    'Tron': 'TRXUSDT',
    'Stellar': 'XLMUSDT',
    'Tezos': 'XTZUSDT',
    'IOTA': 'IOTAUSDT',
    'Neo': 'NEOUSDT'
    # Add more cryptocurrencies as needed
}

def scrap_binance(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    data = response.json()

    if data is not None:
        if 'weightedAvgPrice' in data and 'volume' in data:
            weighted_avg_price = float(data['weightedAvgPrice'])
            volume = float(data['volume'])
            market_cap = weighted_avg_price * volume
            data['marketCap'] = market_cap

        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(f"Empty symbol: {symbol}")

    return data

def main(crypto):
    with ThreadPoolExecutor() as executor:
        futures = []
        for symbol in crypto.values():
            futures.append(executor.submit(scrap_binance, symbol))
        
        for future in futures:
            future.result()
    time.sleep(60)  # Sleep for 5 seconds

if __name__ == "__main__":
    try:
        while True:
            main(crypto)
    except KeyboardInterrupt:
        pass