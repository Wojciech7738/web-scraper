import csv

class FileReaderWriter:
    def __init__(self):
        import os
        project_path = os.path.join(os.getcwd(), "web-scrapper")
        self.input_file_name = os.path.join(project_path, "input/companies.txt")
        self.output_file_name = os.path.join(project_path, "output/dog_cat_food_companies.csv")

    def read_from_txt(self):
        """
        Reads URLs of dog/cat food's companies from TXT file
        """
        try:
            with open(self.input_file_name, "r") as file:
                lines = file.readlines()
        except Exception as e:
            raise e
        return lines
    
    def save_to_csv(self, data):
        """
        Saves extracted company data to a CSV file.
        Args:
            data (list): List of dictionaries containing company data.
        """
        with open(self.output_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'nip'])
            writer.writeheader()
            writer.writerows(data)