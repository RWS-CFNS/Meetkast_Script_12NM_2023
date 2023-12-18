import time
from datetime import datetime
import subprocess

def run_measurement_scripts():
    # Voer MEASUREMENT.py uit
    subprocess.run(["python", "MEASUREMENT.py"])

def run_measuringbox_scripts():
    # Voer MEASURINGBOX.py uit
    subprocess.run(["python", "MEASURINGBOX.py"])

def run_weather_measurement_scripts():
    # Voer WEATHER_MEASUREMENT.py uit
    subprocess.run(["python", "WEATHER_MEASUREMENT.py"])

def main():
    # Aantal seconden in 15 minuten
    interval_seconds = 15 * 60

    while True:
        print(f"Uitvoeren van metingsscripts op: {datetime.now()}")
        
        # Voer de verschillende scripts uit
        run_measurement_scripts()
        run_measuringbox_scripts()
        run_weather_measurement_scripts()
        
        # Wacht 15 minuten voordat de scripts opnieuw worden uitgevoerd
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
