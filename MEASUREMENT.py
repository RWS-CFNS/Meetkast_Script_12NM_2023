import psycopg2
import pika
import json
import time

LAST_PROCESSED_ID_FILE = "last_processed_id_measurement.txt" # Dit stukje initialiseert een variabele met de waarde "last_processed_id.txt".Deze variabele wordt gebruikt om de bestandsnaam op te slaan waarin het laatst verwerkte ID wordt opgeslagen of bijgehouden. 

def get_last_processed_id():
    try:
        with open(LAST_PROCESSED_ID_FILE, "r") as file:  # Opent het bestand LAST_PROCESSED_ID_FILE in leesmodus
            last_processed_id = int(file.read().strip())  # Leest de inhoud van het bestand en converteert het naar een integer
            return last_processed_id  # Geeft de gelezen ID terug
    except FileNotFoundError:  # Vangt een 'FileNotFoundError' op als het bestand niet wordt gevonden
        return 0  # Als het bestand niet wordt gevonden, wordt standaardwaarde 0 geretourneerd

def save_last_processed_id(last_processed_id):
    # Opent het bestand 'LAST_PROCESSED_ID_FILE' om te schrijven ('w' betekent schrijven)
    with open(LAST_PROCESSED_ID_FILE, "w") as file:
        # Schrijft de waarde van 'last_processed_id' naar het geopende bestand
        file.write(str(last_processed_id))

def haal_data_op():
    last_processed_id = get_last_processed_id()  # Ophalen van het laatst verwerkte ID uit een bestand
    
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

        # Query uitvoeren voor 'measurement'
        cur.execute('SELECT * FROM personen.measurement WHERE id > %s;', (last_processed_id,))  # Uitvoeren van een query om rijen op te halen met een ID groter dan het laatst verwerkte ID

        # Gebruik een generator om rijen één voor één op te halen
        for row in cur:
            row_id = row[-1]  # Het ophalen van het ID uit de laatste kolom van elke rij
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
            yield row_id, data  # Retourneren van het ID afzonderlijk van de data
            time.sleep(2)  # Een korte pauze van 2 seconden
            last_processed_id = row_id  # Bijwerken van het laatst verwerkte ID met het ID van de huidige rij

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
        
        save_last_processed_id(last_processed_id)  # Opslaan van het laatst verwerkte ID in een bestand

def verstuur_data():
    # Oproepen van haal_data_op om de gegevens op te halen
    data_generator = haal_data_op()

    try:
        # Maak een verbinding met de RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Converteer de data naar JSON met nette opmaak (inspringing)
        for id_, data in data_generator:
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
            print(f"Verzonden bericht met ID {id_}:")
            print(message)

    except pika.exceptions.AMQPError as e:
        print("Fout bij het verzenden van het bericht:", e)

    finally:
        # Sluit de verbinding
        if connection:
            connection.close()

verstuur_data()
