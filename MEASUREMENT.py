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
    # "id": 2003,
    # "time": current_time_iso,  # Gebruik het ISO 8601-formatted string
    # "latency": 100,
    # "upload": 20.00,
    # "download": 50.00,
    # "RSSI": -20,
    # "RSRQ": 1,
    # "RSRP": -100,
    # "SINR": 4,
    # "mnoString": "KPN",
    # "latitude": 51.985276,
    # "longitude": 4.345539

    "id":None,"time":1699957465299,"latency":56,"upload":54.96,"download":24.51,"mnoString":"mollitia","latitude":3.169556,"longitude":3.341578,"rssi":-70,"rsrq":0,"rsrp":0,"sinr":0
}

# Converteer de dictionary naar een JSON string
message = json.dumps(data)

# print(message)

# Stel de berichteigenschappen in
properties = pika.BasicProperties(
    content_type="application/json",
    content_encoding='UTF-8',
    headers={'__TypeId__': 'nl.cfns.entity.Measurement'},
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