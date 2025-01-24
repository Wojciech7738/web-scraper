import csv
from config import Config

class FileReaderWriter:
    def __init__(self):
        self.configuration = Config()
        self.input_file_path = self.configuration.input_file_path
        self.output_file_path = self.configuration.output_file_path

    def read_from_txt(self):
        """
        Reads URLs of dog/cat food's companies from TXT file
        """
        try:
            with open(self.input_file_path, "r") as file:
                lines = file.readlines()
        except Exception as e:
            raise e
        return [line.strip() for line in lines]
    
    def save_to_csv(self, data):
        """
        Saves extracted company data to a CSV file.
        Args:
            data (list): List of dictionaries containing company data.
        """
        with open(self.output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Company', 'NIP', 'CEO'])
            writer.writeheader()
            writer.writerows(data)