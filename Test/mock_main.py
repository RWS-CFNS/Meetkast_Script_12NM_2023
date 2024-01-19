import subprocess

def run_script(script_name):
    """
    Voert het opgegeven script uit met behulp van Python 3 subprocess.run.
    """
    try:
        subprocess.run(["python3", script_name], check=True)
        print(f"{script_name} is succesvol uitgevoerd")
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het uitvoeren van {script_name}: {e}")

MAX_ITERATIONS = 3  # Stel het maximale aantal iteraties in

def custom_sleep(seconds):
    pass  # Hier wordt niets gedaan, zodat de functie geen tijd wacht

def main():
    """
    Voert metingsscripts uit op een bepaald interval.
    """
    # Aantal seconden in 15 minuten
    interval_seconds = 15 * 60
    iterations = 0  # Initialisatie van de iteratieteller

    while iterations < MAX_ITERATIONS:
        # print(f"Uitvoeren van metingsscripts op: {datetime.now()}")
        # Voer de verschillende scripts uit
        run_script("measurement.py")
        run_script("measuringbox.py")
        run_script("weather_measurement.py")
        # Wacht 15 minuten voordat de scripts opnieuw worden uitgevoerd
        custom_sleep(interval_seconds)  # Gebruik de aangepaste sleep functie
        iterations += 1  # Verhoog de iteratieteller

    # Verwijder het exit statement na het beëindigen van de lus
    # print("Maximale iteraties bereikt. Het script wordt beëindigd.")

if __name__ == "__main__":
    main()
