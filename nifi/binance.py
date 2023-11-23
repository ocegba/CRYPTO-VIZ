import websocket
import json
import requests

# Fonction pour envoyer des données à NiFi
def send_to_nifi(data):
    nifi_endpoint = 'https://localhost:8443/nifi/'  # Remplacez par votre endpoint NiFi
    headers = {'Content-Type': 'application/json'}
    payload = {'your_key': data}  # Adapter la structure de données selon vos besoins
    response = requests.post(nifi_endpoint, headers=headers, data=json.dumps(payload))
    print(response.text)

def on_message(ws, message):
    formatted_data = json.loads(message)
    
    send_to_nifi(formatted_data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")

if __name__ == "__main__":
    ws_endpoint = "'wss://stream.binance.com:9443/ws/solusdt@kline_1m"  # Remplacez par l'URL du flux WebSocket Binance
    ws = websocket.WebSocketApp(ws_endpoint,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
