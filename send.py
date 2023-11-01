import pika
import json
from datetime import datetime

def publish_message(channel, message_data):
    # Handmatig omzetten van datetime naar ISO 8601-string
    message_data["time"] = message_data["time"].isoformat()

    message = json.dumps(message_data)
    channel.basic_publish(
        exchange='spring-boot-exchange',
        routing_key='key.cfns.measurement',
        body=message,
        properties=pika.BasicProperties(
            content_type="application/json",
            headers={'TypeId': 'nl.cfns.entity.Measurement'},
            content_encoding='UTF-8',
            delivery_mode=2,  # maak het bericht persistent
        )
    )
    print("Sent", message)

message_data = {
    "id": 2003,
    "time": datetime(2023, 11, 1, 14, 0, 0, 50000),  # Vervang dit met jouw datetime-object
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