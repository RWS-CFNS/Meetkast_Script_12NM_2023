import pika
import json
from datetime import datetime

# Maak een verbinding met de RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Huidige datetime verkrijgen
current_time = datetime.now()

# Convert the datetime object to an ISO 8601 formatted string
current_time_iso = current_time.isoformat()


# Maak een dictionary met je data
data = {
    "id": 2003,
    "time": current_time_iso,  # Gebruik het ISO 8601-formatted string
    "latency": 1000,
    "upload": 2000,
    "download": 5000,
    "RSSI": -20,
    "RSRQ": 1,
    "RSRP": -100,
    "SINR": 4,
    "mnoString": "KPN",
    "latitude": 51.985276,
    "longitude": 4.345539
}

# Converteer de dictionary naar een JSON string
message = json.dumps(data)

# print(message)

# Stel de berichteigenschappen in
properties = pika.BasicProperties(
    content_type="application/json",
    content_encoding='UTF-8',
    headers={'_TypeId_': 'nl.cfns.entity.Measurement'},
    delivery_mode=2,  # maak het bericht persistent
    priority=0
)

# Stuur het bericht
channel.basic_publish(
    exchange='spring-boot-exchange',
    routing_key='key.cfns.measurement',
    body=message,
    properties=properties
)

print(" [x] Sent %r" % message)

# Sluit de verbinding
connection.close()