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
  # "id": None,
  # "time": current_time,
  # "temp": 25.3,
  # "humid": 68.7,
  # "windDirection": 45,
  # "windspeed": 10,
  # "dauw": 15.8,
  # "pressure": 1012.5

  "time":current_time,
  "temp":71.3,
  "humid":1.0,
  "windDirection":23,
  "windspeed":10.8,
  "dauw":57.0,
  "pressure":97.2
}

# Converteer de dictionary naar een JSON string
message = json.dumps(data)

# print(message)

# Stel de berichteigenschappen in
properties = pika.BasicProperties(
    content_type="application/json",
    content_encoding='UTF-8',
    headers={'__TypeId__': 'nl.cfns.dto.WeatherMeasurementDto'},
    delivery_mode=2,  # maak het bericht persistent
    priority=0
)

# Stuur het bericht
channel.basic_publish(
    exchange='spring-boot-exchange',
    routing_key='key.cfns.weather',
    body=message,
    properties=properties
)

print(" [x] Sent %r" % message)

# Sluit de verbinding
connection.close()
