import unittest
from unittest.mock import patch
from your_script import get_last_processed_id

LAST_PROCESSED_ID_FILE = "last_processed_id_weather.txt"

class TestGetLastProcessedId(unittest.TestCase):

    @patch('builtins.open')
    def test_get_last_processed_id(self, mock_open):
        # Simuleer het gedrag van open() en return een mockbestand
        mock_file = mock_open.return_value
        mock_file.read.return_value = "42\n"

        # Test of de functie het verwachte resultaat oplevert
        result = get_last_processed_id()

        # Asserts om te controleren of de verwachte waarde wordt geretourneerd
        self.assertEqual(result, "Laatste ID: 42")

        # Controleer of open() is aangeroepen met het juiste bestand
        mock_open.assert_called_once_with(LAST_PROCESSED_ID_FILE, "r", encoding="utf-8")

if __name__ == '__main__':
    unittest.main()