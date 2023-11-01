# ------ Hieronder staat de uitwerking van RabbitMQ docs

# #!/usr/bin/env python
# import pika

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='hello')

# channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close() 

# ------ Hieronder staat de uitwerking van een JSON-Object versturen 

#!/usr/bin/env python
import pika
import json

# # Maak een Python-dictionary om te converteren naar JSON
# message_data = {
#     'name': 'John Doe',
#     'email': 'johndoe@example.com',
#     'age': 30
# }

# # Converteer het dictionary naar een JSON-string
# message_json = json.dumps(message_data)

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='hello')

# # Verzend het JSON-object als het berichtlichaam
# channel.basic_publish(exchange='', routing_key='hello', body=message_json)
# print(f" [x] Sent JSON: {message_json}")
# connection.close()

# Maak een Python-dictionary om te converteren naar JSON
message_data = {
  "id": 2003,
  "time": "2023-11-01 14:00:00.05",
  "latency": 1000,
  "upload": 2000,
  "download": 5000,
  "RSSI": -20,
  "RSRQ": 1,
  "RSRP": -100,
  "SINR": 4,
  "mnoString": "KPN",
  "latitude": 51.98527662447251,
  "longitude": 4.3455394836358305
}

# Converteer het dictionary naar een JSON-string
message_json = json.dumps(message_data)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='key.cfns.measurement')

# Verzend het JSON-object als het berichtlichaam
channel.basic_publish(exchange='spring-boot-exchange', routing_key='key.cfns.measurement', body=message_json)
print(f" [x] Sent JSON: {message_json}")
connection.close()