import unittest
from unittest.mock import patch, MagicMock
import subprocess

def run_script(script_name):
    try:
        subprocess.run(["python3", script_name], check=True)
        print(f"{script_name} is succesvol uitgevoerd")
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het uitvoeren van {script_name}: {e}")

class TestRunScript(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_script_success(self, mock_subprocess_run):
        # Configureer mock subprocess.run om een succesvolle uitvoer te simuleren zonder fouten
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        script_name = "test_script.py"  # Vervang met de daadwerkelijke naam van het testscript

        # Roep de functie aan die het script uitvoert
        run_script(script_name)

        # Controleer of subprocess.run correct is aangeroepen met de juiste argumenten
        mock_subprocess_run.assert_called_once_with(["python3", script_name], check=True)

    @patch('subprocess.run')
    def test_run_script_error(self, mock_subprocess_run):
        # Configureer mock subprocess.run om een CalledProcessError te simuleren
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "test_script.py")

        script_name = "test_script.py"  # Vervang met de daadwerkelijke naam van het testscript

        # Roep de functie aan die het script uitvoert
        run_script(script_name)

        # Controleer of subprocess.run correct is aangeroepen met de juiste argumenten
        mock_subprocess_run.assert_called_once_with(["python3", script_name], check=True)

if __name__ == "__main__":
    unittest.main()
