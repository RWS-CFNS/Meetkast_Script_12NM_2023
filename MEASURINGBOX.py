import pika
import json
from datetime import datetime
import time

# Maak een verbinding met de RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Huidige datum en tijd ophalen
current_time = int(time.time()) 
# Dit geeft de huidige tijd in Unix-epoch (seconden sinds 1 januari 1970)

# Maak een dictionary met je data
data = {

"id":None,"mnc":5,"mcc":6,"lac":2,"longitude":48.03,"status":"INACTIVE","latitude":49.5,"simulated":True

}

# Converteer de dictionary naar een JSON string
message = json.dumps(data)

# print(message)

# Stel de berichteigenschappen in
properties = pika.BasicProperties(
    content_type="application/json",
    content_encoding='UTF-8',
    headers={'__TypeId__': 'nl.cfns.entity.Measuringbox'},
    delivery_mode=2,  # maak het bericht persistent
    priority=0
)

# Stuur het bericht
channel.basic_publish(
    exchange='spring-boot-exchange',
    routing_key='key.cfns.measuringbox',
    body=message,
    properties=properties
)

print(" [x] Sent %r" % message)

# Sluit de verbinding
connection.close()