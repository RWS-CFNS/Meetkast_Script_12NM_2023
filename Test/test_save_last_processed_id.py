import unittest
from unittest.mock import patch, mock_open

# De functie die je wilt testen
LAST_PROCESSED_ID_FILE = "test_last_processed_id.txt"  # Een fictieve bestandsnaam

def save_last_processed_id(last_processed_id):
    """
    Save the last processed ID to the file.
    """
    with open(LAST_PROCESSED_ID_FILE, "w", encoding="utf-8") as file:
        file.write(str(last_processed_id))

class TestSaveLastProcessedId(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_save_last_processed_id_success(self, mock_file_open):
        test_id = 123  # Het test-ID dat we willen schrijven

        # Roep de functie aan die het ID naar het bestand schrijft
        save_last_processed_id(test_id)

        # Controleer of het bestand correct is geopend en het juiste ID is geschreven
        mock_file_open.assert_called_once_with(LAST_PROCESSED_ID_FILE, "w", encoding="utf-8")
        mock_file_open().write.assert_called_once_with(str(test_id))

    @patch("builtins.open", new_callable=mock_open)
    def test_save_last_processed_id_file_error(self, mock_file_open):
        # Simuleer een fout bij het openen van het bestand
        mock_file_open.side_effect = IOError

        # Controleer of de functie de fout afhandelt bij het openen van het bestand
        with self.assertRaises(IOError):
            save_last_processed_id(50)  # Probeer een ID te schrijven terwijl het bestand niet kan worden geopend

if __name__ == "__main__":
    unittest.main()
