# Importeer de psycopg2-bibliotheek voor het werken met PostgreSQL-databases
import psycopg2

# Importeer de pika-bibliotheek voor het werken met RabbitMQ
import pika

# Importeer de json-bibliotheek voor het werken met JSON-gegevens
import json

# Importeer de time-bibliotheek voor het beheren van tijdgerelateerde operaties
import time

# Definieer een bestandsnaam voor het opslaan van het laatst verwerkte ID in een tekstbestand
LAST_PROCESSED_ID_FILE = "last_processed_id_weather.txt"

# Definieer een functie om het laatst verwerkte ID uit het tekstbestand op te halen
def get_last_processed_id():
    try:
        # Probeer het tekstbestand te openen en het laatst verwerkte ID te lezen
        with open(LAST_PROCESSED_ID_FILE, "r") as file:
            last_processed_id = int(file.read().strip())
            return last_processed_id
    # Als het tekstbestand niet wordt gevonden, retourneer dan 0
    except FileNotFoundError:
        return 0

# Definieer een functie om het laatst verwerkte ID in het tekstbestand op te slaan
def save_last_processed_id(last_processed_id):
    # Open het tekstbestand en schrijf het laatst verwerkte ID
    with open(LAST_PROCESSED_ID_FILE, "w") as file:
        file.write(str(last_processed_id))


def haal_data_op():
    # Ophalen van het laatst verwerkte ID uit een extern bestand
    last_processed_id = get_last_processed_id()

    try:
        # Een verbinding maken met de database
        conn = psycopg2.connect(
            dbname="test_db",
            user="postgres",
            password="stagecfns",
            host="127.0.0.1"
        )
        # Printen van de verbindingsstatus
        print("Verbindingsstatus:", conn.status)
        # Cursor maken om query's uit te voeren
        cur = conn.cursor()

        # Uitvoeren van een query om rijen op te halen met ID's groter dan het laatst verwerkte ID
        cur.execute('SELECT * FROM personen.weather_measurement WHERE id > %s;', (last_processed_id,))

        # Itereren door elke rij die is opgehaald
        for row in cur:
            # Omzetten van een UNIX-tijd naar een integer
            unix_time = int(row[1].timestamp())
            # Creëren van een data-dictionary met de opgehaalde informatie
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
            # Yielden van het ID en de data
            yield row[0], data
            # Wachten voordat de volgende rij wordt opgehaald
            time.sleep(2)
            # Updaten van het laatst verwerkte ID met het ID van de huidige rij
            last_processed_id = row[0]

    except psycopg2.Error as e:
        # Weergeven van een foutmelding als er een fout optreedt bij de query-uitvoering
        print("Fout bij het uitvoeren van de query voor 'weather_measurement':", e)

    finally:
        try:
            # Sluiten van de cursor en de verbinding
            if cur:
                cur.close()
            if conn:
                conn.close()
        except NameError:
            pass

        # Opslaan van het laatst verwerkte ID in een extern bestand
        save_last_processed_id(last_processed_id)

# Definieert een functie 'verstuur_data()' om gegevens te verzenden.
def verstuur_data():
    # Haalt een generator op met gegevens van haal_data_op() functie.
    data_generator = haal_data_op()

    try:
        # Maakt een verbinding met RabbitMQ-server.
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Itereert door de gegevens die zijn gegenereerd.
        for id_, data in data_generator:
            # Converteert gegevens naar JSON-formaat.
            message = json.dumps(data, indent=4)

            # Stelt eigenschappen van het bericht in voor RabbitMQ.
            properties = pika.BasicProperties(
                content_type="application/json",
                content_encoding='UTF-8',
                headers={'__TypeId__': 'nl.cfns.entity.WeatherMeasurement'},
                delivery_mode=2,
                priority=0
            )

            # Verzendt het bericht via RabbitMQ.
            channel.basic_publish(
                exchange='spring-boot-exchange',
                routing_key='key.cfns.weather',
                body=message,
                properties=properties
            )

            # Toont informatie over het verzonden bericht.
            print(f"Verzonden bericht voor ID {id_}:")
            print(message)

    # Vangt mogelijke RabbitMQ-fouten op.
    except pika.exceptions.AMQPError as e:
        print("Fout bij het verzenden van het bericht:", e)

    # Sluit de verbinding, ongeacht of er een fout is opgetreden.
    finally:
        if connection:
            connection.close()

# Roep de functie 'verstuur_data()' aan om gegevens te verzenden.
verstuur_data()
