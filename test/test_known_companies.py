import unittest
import subprocess
import time
import os, sys

OUTPUT_FILE_PATH = "output/dog_cat_food_companies.csv"
INPUT_FILE_PATH = "input/companies.txt"

class TestWebScraper(unittest.TestCase):
    """
    Test case for verifying the output of the web scraper.
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.input_line_count = get_input_file_line_count()

    @classmethod
    def setUpClass(cls):
        """
        Runs the main script with 'Default File' arguments before all tests.
        """
        line_count = get_input_file_line_count()
        if line_count <= 0:
            print(f"The file {INPUT_FILE_PATH} is empty.")
            sys.exit(1)
        try:
            # Set CWD
            os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
            result = subprocess.run(
                ["python", "src/main.py", "Default", "File"],
                check=True,
                text=True,
                capture_output=True
            )
            print("Script executed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running script.")
            print(e.stderr)
            raise RuntimeError("Script execution failed")
        time.sleep(2)

    def test_output_file_line_count(self):
        """
        Checks if the output file contains exactly {INPUT_FILE_LEN} lines.
        """
        expected_line_count = self.input_line_count + 1
        try:
            with open(OUTPUT_FILE_PATH, "r", encoding="utf-8") as file:
                line_count = sum(1 for _ in file)
            self.assertEqual(line_count, expected_line_count, f"Expected {expected_line_count} lines, but found {line_count}.")
        except Exception as e:
            raise e


def get_input_file_line_count():
    """
    Gets the number of lines in the input file.
    Return value:
        the line count.
    """
    with open(INPUT_FILE_PATH, "r", encoding="utf-8") as file:
        line_count = sum(1 for _ in file)
    return line_count


if __name__ == "__main__":
    unittest.main()
