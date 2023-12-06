# import psycopg2

# # Verbinding maken met de database
# conn = psycopg2.connect(
#     dbname="test_db",
#     user="postgres",
#     password="stagecfns",
#     host="127.0.0.1"  # of het IP-adres van de database
# )

# # Cursor maken om query's uit te voeren
# cur = conn.cursor()

# # Voorbeeldquery om data op te halen
# # query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'personen'"
# query = "SELECT * FROM personen.persoonsgegevens"

# # Uitvoeren van de query
# cur.execute(query)

# # Alle rijen ophalen
# rows = cur.fetchall()

# # Resultaten tonen
# for row in rows:
#     print(row)

# # Verbinding sluiten
# cur.close()
# conn.close()

import psycopg2

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

# Query om aantal rijen in de 'personen'-tabel te controleren
cur.execute('SELECT COUNT(*) FROM public.personen;')
count = cur.fetchone()[0]

if count == 0:
    print("De 'personen'-tabel is leeg.")
else:
    print(f"Aantal rijen in 'personen'-tabel: {count}")

# Query om gegevens uit de 'personen'-tabel op te halen
cur.execute('SELECT * FROM public.personen;')

# Alle rijen ophalen
rows = cur.fetchall()

# Resultaten tonen
if rows:
    for row in rows:
        print(row)
else:
    print("Geen gegevens gevonden in de 'personen'-tabel.")

# Verbinding sluiten
cur.close()
conn.close()

# cfns@cfns-NUC8i7BEH:~/Documents/GitHub/Meetkast_Script_12NM_2023$ python3 Haal_Data.py
# Verbindingsstatus: 1
# De 'personen'-tabel is leeg.
# Geen gegevens gevonden in de 'personen'-tabel.