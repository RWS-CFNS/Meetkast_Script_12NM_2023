import unittest
from unittest.mock import patch

# De functie die je wilt testen
def get_last_processed_id():
    """
    Retrieve the last processed ID from the file.
    """
    try:
        with open("LAST_PROCESSED_ID_FILE", "r", encoding="utf-8") as file:
            last_processed_id = int(file.read().strip())
            return last_processed_id
    except FileNotFoundError:
        return 0

class TestGetLastProcessedId(unittest.TestCase):

    @patch("builtins.open", create=True)
    def test_get_last_processed_id_file_not_found(self, mock_open):
        # Mock het bestand dat niet gevonden wordt
        mock_open.side_effect = FileNotFoundError
        
        # Test of het retourneren van 0 correct is bij een FileNotFound
        result = get_last_processed_id()
        self.assertEqual(result, 0)

    @patch("builtins.open")
    def test_get_last_processed_id_success(self, mock_open):
        # Mock het bestand en retourneer een voorbeeldwaarde
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = "123"  # Een voorbeeldwaarde voor het gelezen ID
        
        # Test of het ID correct wordt geretourneerd
        result = get_last_processed_id()
        self.assertEqual(result, 123)  # Controleer of het geretourneerde ID overeenkomt met wat is gemockt

if __name__ == "__main__":
    unittest.main()
