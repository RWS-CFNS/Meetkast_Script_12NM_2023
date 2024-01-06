"""
Module to handle measurement data retrieval and transmission.
"""

import time
from datetime import datetime
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

def main():
    """
    Voert metingsscripts uit op een bepaald interval.
    """
    # Aantal seconden in 15 minuten
    interval_seconds = 15 * 60

    try:
        while True:
            print(f"Uitvoeren van metingsscripts op: {datetime.now()}")
            # Voer de verschillende scripts uit
            run_script("measurement.py")
            run_script("measuringbox.py")
            run_script("weather_measurement.py")
            # Wacht 15 minuten voordat de scripts opnieuw worden uitgevoerd
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("De test is voltooid.")

if __name__ == "__main__":
    main()
