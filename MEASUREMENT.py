import psycopg2
import pika
import json
import time
import decimal

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

        # Query uitvoeren voor 'Measuringbox'
        cur.execute('SELECT * FROM personen.measurement;')

        # Gebruik een generator om rijen één voor één op te halen
        for row in cur:
            # Unix-epoch conversie
            unix_time = int(row[0].timestamp())
            # Omzetten naar dictionary-formaat
            data = {
                "id": None,  # Toevoegen van 'id' met waarde 'None'
                "time": unix_time,  # Zet datetime om naar string
                "latency": float(row[1]),  # Zet Decimal om naar float
                "upload": float(row[2]),  # Zet Decimal om naar float
                "download": float(row[3]),  # Zet Decimal om naar float
                "mnoString": row[4],
                "latitude": float(row[5]),  # Zet Decimal om naar float
                "longitude": float(row[6]),  # Zet Decimal om naar float
                "rssi": float(row[7]),  # Zet Decimal om naar float
                "rsrq": float(row[8]),  # Zet Decimal om naar float
                "rsrp": float(row[9]),  # Zet Decimal om naar float
                "sinr": float(row[10])  # Zet Decimal om naar float
            }
            yield data
            # Wacht 5 seconden voordat je de volgende rij ophaalt
            time.sleep(5)

    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'measurement':", e)
    
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
                headers={'__TypeId__': 'nl.cfns.entity.Measurement'},
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
