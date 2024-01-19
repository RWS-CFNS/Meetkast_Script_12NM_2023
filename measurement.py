"""
Module to handle measurement data retrieval and transmission.
"""

import json
import time
import psycopg2
import pika

LAST_PROCESSED_ID_FILE = "last_processed_id_measurement.txt"


def get_last_processed_id():
    """
    Retrieve the last processed ID from the file.
    """
    try:
        with open(LAST_PROCESSED_ID_FILE, "r", encoding="utf-8") as file:
            last_processed_id = int(file.read().strip())
            return last_processed_id
    except FileNotFoundError:
        return 0


def save_last_processed_id(last_processed_id):
    """
    Save the last processed ID to the file.
    """
    with open(LAST_PROCESSED_ID_FILE, "w", encoding="utf-8") as file:
        file.write(str(last_processed_id))


def retrieve_data():
    """
    Retrieve measurement data from the database.
    """
    last_processed_id = get_last_processed_id()

    try:
        conn = psycopg2.connect(
            dbname="test_db",
            user="postgres",
            password="stagecfns",
            host="127.0.0.1"
        )
        print("Verbindingsstatus:", conn.status)
        cur = conn.cursor()

        cur.execute('SELECT * FROM personen.measurement WHERE id > %s;', (last_processed_id,))

        for row in cur:
            row_id = row[-1]
            unix_time = int(row[0].timestamp())
            data = {
                "id": None,
                "time": unix_time,
                "latency": float(row[1]),
                "upload": float(row[2]),  
                "download": float(row[3]),   
                "mnoString": row[4],
                "latitude": float(row[5]),  
                "longitude": float(row[6]),  
                "rssi": float(row[7]),  
                "rsrq": float(row[8]),  
                "rsrp": float(row[9]),  # Zet Decimal om naar float
                "sinr": float(row[10])
            }
            yield row_id, data
            time.sleep(2)
            last_processed_id = row_id

    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'measurement':", e)

    finally:
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except NameError:
            pass

        save_last_processed_id(last_processed_id)


def send_data():
    """
    Send measurement data to the RabbitMQ server.
    """
    data_generator = retrieve_data()

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        for id_, data in data_generator:
            message = json.dumps(data, indent=4)

            properties = pika.BasicProperties(
                content_type="application/json",
                content_encoding='UTF-8',
                headers={'__TypeId__': 'nl.cfns.entity.Measurement'},
                delivery_mode=2,
                priority=0
            )

            channel.basic_publish(
                exchange='spring-boot-exchange',
                routing_key='key.cfns.measurement',
                body=message,
                properties=properties
            )

            print(f"Verzonden bericht met ID {id_}:")
            print(message)

    except pika.exceptions.AMQPError as e:
        print("Fout bij het verzenden van het bericht:", e)

    finally:
        if connection:
            connection.close()


send_data()
