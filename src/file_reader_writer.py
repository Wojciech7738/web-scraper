import csv
from config import Config

class FileReaderWriter:
    def __init__(self):
        self.configuration = Config()
        self.input_file_path = self.configuration.input_file_path
        self.api_key_file_path = self.configuration.api_key_file_path
        self.output_file_path = self.configuration.output_file_path

    def read_from_txt(self, get_api_key=False):
        """
        Reads URLs of dog/cat food's companies from TXT file (input/companies.txt)
        or the GUS API key from input/api_key.txt
        """
        path = self.api_key_file_path if get_api_key else self.input_file_path
        try:
            with open(path, "r") as file:
                lines = file.readlines()
        except Exception as e:
            raise e
        return [line.strip() for line in lines]
    
    def save_to_csv(self, data):
        """
        Saves extracted company data to a CSV file.
        Args:
            data (list): List of tuples containing companies data.
        """
        dict_data = [{'Company': item[0], 'NIP': item[1], 'CEO': item[2]} for item in data]
        with open(self.output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Company', 'NIP', 'CEO'])
            writer.writeheader()
            writer.writerows(dict_data)