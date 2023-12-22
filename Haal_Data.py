import psycopg2

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

    # Query en try-except voor 'naam_leeftijd'
    try:
        cur.execute('SELECT COUNT(*) FROM personen.naam_leeftijd;')
        count = cur.fetchone()[0]

        if count == 0:
            print("De 'naam_leeftijd'-tabel is leeg.")
        else:
            print(f"Aantal rijen in 'naam_leeftijd'-tabel: {count}")

        cur.execute('SELECT * FROM personen.naam_leeftijd;')
        rows = cur.fetchall()

        if rows:
            print("\nData uit 'naam_leeftijd' tabel:")
            for row in rows:
                print(row)
        else:
            print("Geen gegevens gevonden in de 'naam_leeftijd'-tabel.")
    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'naam_leeftijd':", e)

    # Query en try-except voor 'Measuringbox'
    try:
        cur.execute('SELECT COUNT(*) FROM personen.measuringbox;')
        count = cur.fetchone()[0]

        if count == 0:
            print("De 'measuringbox'-tabel is leeg.")
        else:
            print(f"Aantal rijen in 'measuringbox'-tabel: {count}")

        cur.execute('SELECT * FROM personen.measuringbox;')
        rows = cur.fetchall()

        if rows:
            print("\nData uit 'measuringbox' tabel:")
            for row in rows:
                print(row)
        else:
            print("Geen gegevens gevonden in de 'measuringbox'-tabel.")
    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'measuringbox':", e)

    # Query en try-except voor 'Weather_Measurement'
    try:
        cur.execute('SELECT COUNT(*) FROM personen.weather_measurement;')
        count = cur.fetchone()[0]

        if count == 0:
            print("De 'weather_measurement'-tabel is leeg.")
        else:
            print(f"Aantal rijen in 'weather_measurement'-tabel: {count}")

        cur.execute('SELECT * FROM personen.weather_measurement;')
        rows = cur.fetchall()

        if rows:
            print("\nData uit 'weather_measurement' tabel:")
            for row in rows:
                print(row)
        else:
            print("Geen gegevens gevonden in de 'weather_measurement'-tabel.")
    except psycopg2.Error as e:
        print("Fout bij het uitvoeren van de query voor 'weather_measurement':", e)

    # Verbinding sluiten
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Verbindingsfout:", e)
