import requests

crypto=['CYBERUSDT','BTCUSDT']

def get_crypto_price(crypto):
    for i in crypto:
        x = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={i}")
        print(x.status_code)
        print(x.text)
        result = x.json()

get_crypto_price(crypto)