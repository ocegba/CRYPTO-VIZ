import requests

def get_binance_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()

    binance_data = {item['symbol']: item for item in data}

    return binance_data

def get_crypto_info(binance_data, symbol):
    if symbol in binance_data:
        return binance_data[symbol]
    else:
        return None

# Fetch Binance data
binance_data = get_binance_data()

# Get information for BTC
btc_info = get_crypto_info(binance_data, "BTCUSDT")

if btc_info is not None:
    print("BTC Information:")
    for key, value in btc_info.items():
        print(f"{key}: {value}")
else:
    print("BTC data not found.")
