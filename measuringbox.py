"""
Module to handle measurement data retrieval and transmission.
"""

import json
import time
import psycopg2
import pika

LAST_PROCESSED_ID_FILE = "last_processed_id_measuringbox.txt"

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


def haal_data_op():
    """
    Retrieve measurement data from the database.
    """
    last_processed_id = get_last_processed_id()

    try:
        conn = psycopg2.connect(  # Verbinding maken met de database
            dbname="test_db",
            user="postgres",
            password="stagecfns",
            host="127.0.0.1"
        )
        print("Verbindingsstatus:", conn.status)  # Afdrukken van de verbindingsstatus
        cur = conn.cursor()  # Cursor maken om query's uit te voeren

        cur.execute('SELECT * FROM personen.measuringbox WHERE id > %s;', (last_processed_id,))  # Uitvoeren van een query om rijen op te halen met een ID groter dan het laatst verwerkte ID

        for row in cur:  # Itereren over de opgehaalde rijen
            row_id = row[-1]  # Het ophalen van het ID uit de laatste kolom van elke rij
            data = {
                "id": None,  # Toevoegen van 'id' met waarde 'None' aan de data dictionary
                "mnc": row[0],
                "mcc": row[1],
                "lac": row[2],
                "longitude": row[3],
                "status": row[4],
                "latitude": row[5],
            }
            yield row_id, data
            time.sleep(2)
            last_processed_id = row_id

    except psycopg2.Error as e:  # Het afhandelen van een PostgreSQL-fout
        print("Fout bij het uitvoeren van de query voor 'measuringbox':", e)

    finally:  # De final block wordt altijd uitgevoerd
        try:
            if cur:
                cur.close()  # Sluiten van de cursor
            if conn:
                conn.close()  # Sluiten van de databaseverbinding
        except NameError:
            pass  # Afhandelen van een NameError als die optreedt

        save_last_processed_id(last_processed_id)

# De functie 'verstuur_data' wordt gedefinieerd
def verstuur_data():
    """
    Send measurement data to the RabbitMQ server.
    """

    # De generator 'data_generator' wordt aangemaakt door de functie 'haal_data_op' op te roepen
    data_generator = haal_data_op()

    # Een poging wordt gedaan om een verbinding met RabbitMQ te maken
    try:
        # Een verbinding en kanaal worden opgezet met de lokale RabbitMQ-server
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Itereren over de gegenereerde data en ID's
        for id_, data in data_generator:
            # De data wordt omgezet naar een JSON-bericht met nette opmaak
            message = json.dumps(data, indent=4)
            # De berichteigenschappen worden ingesteld
            properties = pika.BasicProperties(
                content_type="application/json",
                content_encoding='UTF-8',
                headers={'__TypeId__': 'nl.cfns.entity.Measuringbox2'},
                delivery_mode=2,  # Maak het bericht persistent
                priority=0
            )

            channel.basic_publish(
                exchange='spring-boot-exchange',
                routing_key='key.cfns.measuringbox2',
                body=message,
                properties=properties
            )

            # Een bericht wordt afgedrukt om aan te geven dat het bericht is verzonden
            print(f"Verzonden bericht voor ID {id_}:")
            print(message)

    # Een except-blok om eventuele fouten bij het verzenden van het bericht af te handelen
    except pika.exceptions.AMQPError as e:
        print("Fout bij het verzenden van het bericht:", e)

    # Een finally-blok om de verbinding te sluiten, ongeacht of er fouten zijn opgetreden of niet
    finally:
        if connection:
            connection.close()

# De functie 'verstuur_data' wordt opgeroepen om het script uit te voeren
verstuur_data()
