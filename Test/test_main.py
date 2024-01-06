# from unittest import TestCase
# from datetime import datetime, timedelta
# from mock_main import main

# class TestMainFunction(TestCase):

#     def test_run_measurement_scripts(self):
#         start_time = datetime.now()
#         main()
#         end_time = datetime.now()

#         # Bereken het verschil in tijd
#         time_difference = end_time - start_time

#         # Controleer of de tijd tussen de start en eindtijd minder dan 15 minuten is
#         self.assertLessEqual(time_difference, timedelta(minutes=15))

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import time
import subprocess

# importeer de module mock_main
import mock_main

class TestMainFunction(unittest.TestCase):
    @patch("mock_main.run_script")
    def test_run_scripts_called(self, mock_run_script):
        # Start de main functie van mock_main
        mock_main.main()

        # Controleer of run_script is aangeroepen met de juiste argumenten
        expected_calls = [
            ("measurement.py",),
            ("measuringbox.py",),
            ("weather_measurement.py",)
        ]
        actual_calls = [call[0] for call in mock_run_script.call_args_list]

        self.assertEqual(actual_calls, expected_calls)

if __name__ == "__main__":
    unittest.main()
