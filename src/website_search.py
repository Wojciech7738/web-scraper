from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from bs4 import BeautifulSoup

class WebsiteSearch:
    def __init__(self):
        # Configure Selenium WebDriver
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.nip_pattern = r"\d{3}-\d{2}-\d{2}-\d{2}|\d{9,10}"
        self.ceo_pattern = r"prezes"
        self.ceo_value_pattern = r"[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?: [A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)+"
    
    
    def _enter_sublink_on_website(self, company_name):
        # Collect all links
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        # Print all links in the results
        results = soup.find_all("a")
        if not results:
            print("No results found.")
            return None
        # Create regex pattern from company name (spaces can be replaced with something else on the website)
        pattern = company_name.lower().replace(" ", r".*")
        # Iterate through results and find the matching link
        for result in results:
            link_text = result.get_text(strip=True).lower()
            if re.findall(pattern, link_text):
                href = result.get("href")
                print(f"Found matching link: {link_text} -> {href}")
                # Click the link using Selenium
                self.driver.get(f"https://rejestr.io{href}")
                break
        else:
            print(f"No matching link found for company: {company_name}")
            return None
    
    def find_company_data(self, company_name):
        """
        Fetches the NIP of a company by searching Google.
        Args:
            company_name (str): The name of the company.
        Returns:
            str: The NIP of the company, or 'Not found' if unavailable.
        """
        try:
            # TODO: replace with link
            self.driver.get("https://rejestr.io/")
            search_box = self.driver.find_element(By.NAME, "q")
            search_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.send_keys(company_name)
            search_box.send_keys(Keys.RETURN)
            # Wait until the page is loaded
            self._wait_for_page()
            # TODO: use it if there is no info on the current site - SEARCH NIP FIRST
            # TODO: if not results:
            results = self._enter_sublink_on_website(company_name)
            self._wait_for_page()
            
            # Wait for the page to load and find the NIP
            nip = self.fetch_nip_from_page(self.driver.page_source, "NIP")
            ceo = self.fetch_ceo_from_page(self.driver.page_source, "PREZES")
            return (company_name, nip, ceo)
        except Exception as e:
            print(f"Error fetching NIP for {company_name}: {e}")
        return None
    
    def close(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()

    def _wait_for_page(self):
        time.sleep(1) # TODO: get rid of it maybe?
        try:
            WebDriverWait(self.driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
        except Exception as e:
            del e

    def fetch_nip_from_page(self, page_source, text_to_find):
        """
        Extracts the text_to_find (NIP or CEO) from the HTML source of a company's page.
        
        Args:
            page_source (str): The HTML source of the company's page.
        
        Returns:
            str: The text_to_find if found, otherwise '{text_to_find} not found'.# TODO
        """
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Look for a tag containing text_to_find (adjust selector based on actual structure)
        found_element = soup.find(string=lambda text: text and text_to_find in text)
        
        if found_element:
            # Check in the same container (parent)
            # If not found, search siblings or other levels
            current = found_element.find_parent()
            while current:
                # Search for NIP in the siblings or parent hierarchy
                text_match = re.search(self.nip_pattern, current.text)
                if text_match:
                    return text_match.group().strip()
                # Move up the tree (go to parent)
                current = current.find_parent()
        
        return None
    

    def fetch_ceo_from_page(self, page_source, text_to_find):
        """
        Extracts the text_to_find (NIP or CEO) from the HTML source of a company's page.
        
        Args:
            page_source (str): The HTML source of the company's page.
        
        Returns:
            str: The text_to_find if found, otherwise '{text_to_find} not found'.#TODO
        """
        text_name_search_function = re.compile(self.ceo_pattern, re.IGNORECASE)
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Look for a tag containing text_to_find (adjust selector based on actual structure)
        found_element = soup.find(string=text_name_search_function)
        
        if found_element:
            # Start from the parent of the found element
            current = found_element.find_parent()
            while current:
                # Iterate over all descendants of the current container
                for descendant in current.find_all(class_="name"):
                    if descendant.name == "p":
                        # Check if the descendant contains text matching the pattern
                        text_match = re.search(self.ceo_value_pattern, descendant.get_text(strip=True))
                        if text_match:
                            # Return the entire content of the matching element
                            return descendant.get_text(strip=True)
                # Move up the tree (to the next parent container)
                current = current.find_parent()
        return None