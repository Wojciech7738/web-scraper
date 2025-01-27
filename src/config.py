import os

class SingletonMeta(type):
    """
    A metaclass for creating singleton classes.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# A class for holding the whole configuration of the project
class Config(metaclass=SingletonMeta):
    def __init__(self):
        project_path = os.path.join(os.getcwd(), "web-scrapper")
        self.project_path = project_path
        self.input_file_path = os.path.join(project_path, "input", "companies.txt")
        self.output_file_path = os.path.join(project_path, "output", "dog_cat_food_companies.csv")
        self.api_key_file_path = os.path.join(project_path, "input", "api_key.txt")
        self.nip_pattern = r"\d{3}-\d{2}-\d{2}-\d{2}|\d{9,10}"
        self.ceo_pattern = r"prezes|zarzad|zarząd|beneficjenci rzeczywiści|beneficjenci rzeczywisci"
        self.ceo_value_pattern = r"^(?:[A-ZŁŚŻ][a-ząćęłńóśźż]{2,}(?:\s[A-ZŁŚŻ][a-ząćęłńóśźż]{2,}){0,2}\s[A-ZĆŁŚŹŻ][a-ząćęłńóśźż]{1,}(?:\-[A-ZĆŁŚŹŻ][a-ząćęłńóśźż]{1,})?)|(?:[A-ZĄĆĘŁŃÓŚŹŻ]{3,}(?:\s[A-ZĄĆĘŁŃÓŚŹŻ]{3,}){0,2}\s[A-ZĄĆĘŁŃÓŚŹŻ]{2,}(?:\-[A-ZĄĆĘŁŃÓŚŹŻ]{2,})?)$"
        self.checking_website_urls = [
            "https://rejestr.io",
            "https://krs-pobierz.pl"
            # "https://panoramafirm.pl"
        ]
        self.company_branch_keywords = ["zwierząt", "spożywcze", "handel detaliczny", "sprzedaż"]

