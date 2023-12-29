import psycopg2
import pika
import json
import time

def haal_data_op():
    try:
        # Verbinding maken met de database
        conn = psycopg2.connect(
            dbname="test_db",
            user="postgres",
            password="stagecfns",
            host="127.0.0.1"  # of het IP-adres van de database
        )

        # Controleren van de verbindingstatus
        print("Verbindingsstatus:", conn.status)

        # Cursor maken om query's uit te voeren
        cur = conn.cursor()

        # Query uitvoeren voor 'measuringbox'
        cur.execute('SELECT * FROM personen.measuringbox;')

        # Gebruik een generator om rijen één voor één op te halen
        for row in cur:
            # Omzetten naar dictionary-formaat
            data = {
                "id": None,  # Toevoegen van 'id' met waarde 'None'
                "mnc": row[0],
                "mcc": row[1],
                "lac": row[2],
                "longitude": row[3],
                "status": row[4],
                "latitude": row[5],
            }
            yield data
            # Wacht 2 seconden voordat je de volgende rij ophaalt
            time.sleep(2)

    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'measuringbox':", e)

    finally:
        # Sluit de cursor en verbinding, ongeacht of er een fout is opgetreden
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except NameError:
            pass

def verstuur_data():
    # Oproepen van haal_data_op om de gegevens op te halen
    data_generator = haal_data_op()

    try:
        # Maak een verbinding met de RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Converteer de data naar JSON met nette opmaak (inspringing)
        for data in data_generator:
            message = json.dumps(data, indent=4)

            # Stel de berichteigenschappen in
            properties = pika.BasicProperties(
                content_type="application/json",
                content_encoding='UTF-8',
                headers={'__TypeId__': 'nl.cfns.entity.Measuringbox2'},
                delivery_mode=2,  # maak het bericht persistent
                priority=0
            )

            # Stuur het bericht
            channel.basic_publish(
                exchange='spring-boot-exchange',
                routing_key='key.cfns.measuringbox2',
                body=message,
                properties=properties
            )

            # Print de verzonden data met nette opmaak
            print("Verzonden bericht:")
            print(message)

    except pika.exceptions.AMQPError as e:
        print("Fout bij het verzenden van het bericht:", e)

    finally:
        # Sluit de verbinding
        if connection:
            connection.close()

verstuur_data()
