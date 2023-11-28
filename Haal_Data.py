import psycopg2

# Verbinding maken met de database
conn = psycopg2.connect(
    dbname="test_db",
    user="postgres",
    password="stagecfns",
    host="127.0.0.1"  # of het IP-adres van de database
)

# Cursor maken om query's uit te voeren
cur = conn.cursor()

# Voorbeeldquery om data op te halen
query = "SELECT * FROM jouw_tabel_naam"

# Uitvoeren van de query
cur.execute(query)

# Alle rijen ophalen
rows = cur.fetchall()

# Resultaten tonen
for row in rows:
    print(row)

# Verbinding sluiten
cur.close()
conn.close()
