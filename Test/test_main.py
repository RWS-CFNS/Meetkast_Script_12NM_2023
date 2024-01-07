import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from datetime import datetime
import mock_main  # Importeer de module waarin je de aangepaste main-functie hebt

class TestMockMain(unittest.TestCase):

    def test_run_script_call_count(self):
        with patch('mock_main.run_script') as mock_run_script:
            # Roep de main-functie aan
            mock_main.main()

            # Controleer het aantal keren dat run_script is aangeroepen
            expected_calls = mock_main.MAX_ITERATIONS * 3  # 3 scripts per iteratie
            self.assertEqual(mock_run_script.call_count, expected_calls)

    def test_output_control(self):
        with patch('mock_main.run_script'), patch('time.sleep') as mock_sleep:
            fake_time = datetime(2024, 1, 7, 12, 0, 0)
            mock_datetime = MagicMock(wraps=datetime)
            mock_datetime.now.return_value = fake_time

            # Voeg de mock_datetime toe aan mock_main
            mock_main.datetime = mock_datetime

            # Capture de uitvoer van print-statements
            captured_output = StringIO()
            import sys
            sys.stdout = captured_output

            # Roep de main-functie aan
            mock_main.main()

            # Controleer of er geen uitvoer is
            self.assertEqual(captured_output.getvalue(), "")

            # Herstel sys.stdout
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
