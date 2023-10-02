from confluent_kafka import Producer
import time

# Callback de livraison pour gérer la livraison ou les erreurs du message
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Configuration du producteur
conf = {
    'bootstrap.servers': 'host.docker.internal:9092',
    'client.id': 'python-producer'
}

producer = Producer(conf)

# Produire un message toutes les secondes
try:
    for i in range(1000):
        value = f"Message {i}"
        producer.produce('test', key=str(i), value=value, callback=delivery_report) # Remplacez 'YOUR_TOPIC' par le nom de votre topic
        producer.poll(0)
        time.sleep(1)

except KeyboardInterrupt:
    pass

# Assurez-vous que tous les messages sont envoyés avant de quitter
producer.flush()
