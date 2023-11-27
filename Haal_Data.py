import psycopg2

# Verbinding maken met de database
conn = psycopg2.connect(
    dbname="jouw_database_naam",
    user="jouw_gebruikersnaam",
    password="jouw_wachtwoord",
    host="localhost"  # of het IP-adres van de database
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
