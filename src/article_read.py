import spacy
import pytextrank

class ArticleReader:
    def __init__(self):
        try:
            # Load the Polish language model
            self.nlp = spacy.load("pl_core_news_sm")
        except Exception as e:
            print("Downloading the Polish language model...")
            self.__download_spacy_model()
        # Add PyTextRank to spaCy pipeline
        self.nlp.add_pipe("textrank")
            
    def __download_spacy_model(self):
        """
        Runs the command to download the spaCy model 'pl_core_news_sm'.
        """
        import subprocess
        try:
            result = subprocess.run(
                ["python", "-m", "spacy", "download", "pl_core_news_sm"],
                check=True,
                text=True,
                capture_output=True
            )
            self.nlp = spacy.load("pl_core_news_sm")
        except Exception as e:
            raise e
        


    def read_companies(self):
        url = "https://technologia-zywnosci.pl/lista-firm-producenci-karmy-dla-zwierzat/"
        phrases = []
        # while len(phrases) <= 10:
        text = self.fetch_polish_brands_text(url)
        if text:
            doc = self.nlp(text)
            phrases = [phrase.text for phrase in doc._.phrases if phrase.text[0].isupper()]
        # Remove unnecessary records
        import re
        pattern = r"Polsce|Polscy|Polskie|Polskich"
        phrases = [p for p in phrases if not re.match(pattern, p)]
        return phrases
    
    def fetch_polish_brands_text(self, url):
        """
        Fetches text under the 'h3' header containing 'Polskie marki' from the given URL.
        
        Args:
            url (str): The URL of the webpage to scrape.
        
        Returns:
            str: The text under the header, or None if not found.
        """
        import requests
        from bs4 import BeautifulSoup
        try:
            # Send a GET request to fetch the webpage
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            response.encoding = "utf-8"

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the <h3> tag containing 'Polskie marki'
            # header = soup.find("h3", string=lambda text: text and "Polskie marki" in text)
            # if header:
            #     # Find the next <p> tag after the <h3>
            #     paragraph = header.find_next("p")
            #     if paragraph:
            #         return paragraph.get_text(strip=True)
            headers = soup.find_all("h3")
            if headers:
                result_text = ""
                for header in headers:
                    # Find the next <p> tag after the <h3>
                    paragraph = header.find_next("p")
                    if paragraph:
                        result_text += paragraph.get_text(strip=True)
                return result_text
                
        except Exception as e:
            return f"An error occurred: {e}"
        return None


# text = """
# Na rynku polskim działają producenci karmy dla zwierząt, tacy jak Dolina Noteci, Vet Expert, Royal Canin czy Purina. 
# Nie można zapomnieć o Hill’s, Josera, Acana i Orijen. To jedni z najlepszych producentów dostępnych na rynku.
# """
