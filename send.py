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

# Maak een Python-dictionary om te converteren naar JSON
message_data = {
    'name': 'John Doe',
    'email': 'johndoe@example.com',
    'age': 30
}

# Converteer het dictionary naar een JSON-string
message_json = json.dumps(message_data)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

# Verzend het JSON-object als het berichtlichaam
channel.basic_publish(exchange='', routing_key='hello', body=message_json)
print(f" [x] Sent JSON: {message_json}")
connection.close()
