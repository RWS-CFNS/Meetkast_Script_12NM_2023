import pika
import json
import time

# Maak een verbinding met de RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Huidige datum en tijd ophalen
current_time = int(time.time()) 
# Dit geeft de huidige tijd in Unix-epoch (seconden sinds 1 januari 1970)

# Maak een dictionary met je data
data = {

    "time":current_time,
    "latency":56,
    "upload":54.96,
    "download":24.51,
    "mnoString":"mollitia",
    "latitude":3.169556,
    "longitude":3.341578,
    "rssi":-70,
    "rsrq":0,
    "rsrp":0,
    "sinr":0
}

# Converteer de dictionary naar een JSON string
message = json.dumps(data)

# print(message)

# Stel de berichteigenschappen in
properties = pika.BasicProperties(
    content_type="application/json",
    content_encoding='UTF-8',
    headers={'__TypeId__': 'nl.cfns.dto.MeasurementDto'},
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