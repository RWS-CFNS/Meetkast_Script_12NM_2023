import pika
import json
from datetime import datetime

def publish_message(channel, message_data):
    message = json.dumps(message_data)
    channel.basic_publish(
        exchange='spring-boot-exchange',
        routing_key='key.cfns.measurement',
        body=message,
        properties=pika.BasicProperties(
            content_type="application/json",
            content_encoding='UTF-8',
            headers={'TypeId': 'nl.cfns.entity.Measurement'},
            delivery_mode=2,  # maak het bericht persistent
            priority=0
        )
    )
    print("Sent", message)

# Huidige datetime verkrijgen
current_time = datetime.now()

# Convert the datetime object to an ISO 8601 formatted string
current_time_iso = current_time.isoformat()

message_data = {
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

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='key.cfns.measurement')

try:
    publish_message(channel, message_data)
except Exception as e:
    print("An error occurred:", str(e))
finally:
    if connection.is_open:
        connection.close()