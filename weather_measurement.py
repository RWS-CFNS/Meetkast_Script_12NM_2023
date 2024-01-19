"""Alle benodigden imports."""
import json
import time
import psycopg2
import pika

LAST_PROCESSED_ID_FILE = "last_processed_id_weather.txt"

def get_last_processed_id():
    try:
        with open(LAST_PROCESSED_ID_FILE, "r", encoding="utf-8") as file:
            last_processed_id = int(file.read().strip())
            return last_processed_id
    except FileNotFoundError:
        return 0

def save_last_processed_id(last_processed_id):
    """Slaat het laatst verwerkte ID op in het tekstbestand."""
    with open(LAST_PROCESSED_ID_FILE, "w", encoding="utf-8") as file:
        file.write(str(last_processed_id))

def haal_data_op():
    """Haalt gegevens op uit de database."""
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

        cur.execute('SELECT * FROM personen.weather_measurement WHERE id > %s;', (last_processed_id,))

        for row in cur:
            unix_time = int(row[1].timestamp())
            data = {
                "id": row[0],
                "time": unix_time,
                "temp": float(row[2]),
                "humid": float(row[3]),
                "windDirection": float(row[4]),
                "windspeed": float(row[5]),
                "dauw": float(row[6]),
                "pressure": float(row[7]),
            }
            yield row[0], data
            time.sleep(2)
            last_processed_id = row[0]

    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'weather_measurement':", e)

    finally:
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except NameError:
            pass

        save_last_processed_id(last_processed_id)

def verstuur_data():
    """Verzendt de opgehaalde gegevens via RabbitMQ."""
    data_generator = haal_data_op()

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        for id_, data in data_generator:
            message = json.dumps(data, indent=4)

            properties = pika.BasicProperties(
                content_type="application/json",
                content_encoding='UTF-8',
                headers={'__TypeId__': 'nl.cfns.entity.WeatherMeasurement'},
                delivery_mode=2,
                priority=0
            )

            channel.basic_publish(
                exchange='spring-boot-exchange',
                routing_key='key.cfns.weather',
                body=message,
                properties=properties
            )

            print(f"Verzonden bericht voor ID {id_}:")
            print(message)

    except pika.exceptions.AMQPError as e:
        print("Fout bij het verzenden van het bericht:", e)

    finally:
        if connection:
            connection.close()

verstuur_data()
