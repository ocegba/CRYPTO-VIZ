import requests
from concurrent.futures import ThreadPoolExecutor
import time

crypto = {
    'Bitcoin': 'BTCUSDT',
    # 'Ethereum': 'ETHUSDT',
    # 'Binance Coin': 'BNBUSDT',
    # 'Cardano': 'ADAUSDT',
    # 'Solana': 'SOLUSDT',
    # 'XRP': 'XRPUSDT',
    # 'Polkadot': 'DOTUSDT',
    # 'Dogecoin': 'DOGEUSDT',
    # 'Avalanche': 'AVAXUSDT',
    # 'Chainlink': 'LINKUSDT',
    # 'Litecoin': 'LTCUSDT',
    # 'Bitcoin Cash': 'BCHUSDT',
    # 'Cosmos': 'ATOMUSDT',
    # 'VeChain': 'VETUSDT',
    # 'Filecoin': 'FILUSDT',
    # 'Ethereum Classic': 'ETCUSDT',
    # 'Tron': 'TRXUSDT',
    # 'Stellar': 'XLMUSDT',
    # 'Tezos': 'XTZUSDT',
    # 'IOTA': 'IOTAUSDT',
    # 'Neo': 'NEOUSDT'
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

            data['nvtRatio'] = market_cap / volume

            funding_response = requests.get(f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}")
            funding_data = funding_response.json()
            if funding_data:
                last_funding_rate = funding_data[-1]['fundingRate']  # Get the last funding rate
                data['lastFundingRate'] = last_funding_rate

            open_interest_response = requests.get(f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}")
            open_interest_data = open_interest_response.json()
            if open_interest_data:
                last_open_interest = open_interest_data['openInterest']  # Get the last open interest
                data['lastOpenInterest'] = last_open_interest

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
            # futures.append(executor.submit(get_historical_data, symbol, "1d"))
        
        for future in futures:
            future.result()
    time.sleep(60)  # Sleep for 5 seconds

if __name__ == "__main__":
    try:
        while True:
            main(crypto)
    except KeyboardInterrupt:
        pass