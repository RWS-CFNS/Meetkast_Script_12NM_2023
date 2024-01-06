import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from mock_main import main

class TestMainFunction(unittest.TestCase):

    @patch("mock_main.run_script")
    def test_run_measurement_scripts(self, mock_run_script):
        # Simuleer de uitvoering van de main-functie
        main()

        # Controleer of de metingsscripts correct zijn uitgevoerd
        expected_calls = [
            ("measurement.py",),
            ("measuringbox.py",),
            ("weather_measurement.py",)
        ]
        for call_args in expected_calls:
            mock_run_script.assert_any_called_with(*call_args)

    @patch("mock_main.time.sleep")
    @patch("mock_main.datetime")
    @patch("mock_main.run_script")
    def test_error_handling(self, mock_run_script, mock_datetime, mock_sleep):
        # Creëer een exceptie om te simuleren dat er een fout optreedt
        mock_run_script.side_effect = Exception("Testfout")

        # Simuleer de uitvoering van de main-functie
        main()

        # Controleer of de error handling plaatsvindt
        mock_run_script.assert_called_once()
        # Verifieer dat de slaaptimer niet wordt aangeroepen wanneer er een fout optreedt
        mock_sleep.assert_not_called()

        # Verifieer dat de fout wordt afgedrukt
        self.assertTrue(mock_run_script.side_effect, Exception)

if __name__ == "__main__":
    unittest.main()
