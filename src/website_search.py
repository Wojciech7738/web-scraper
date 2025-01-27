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
        from config import Config
        configuration = Config()
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.nip_pattern = configuration.nip_pattern
        self.ceo_pattern = configuration.ceo_pattern
        self.ceo_value_pattern = configuration.ceo_value_pattern
        self.checking_website_urls = configuration.checking_website_urls
        self.company_branch_keywords = configuration.company_branch_keywords

    def close(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()
    
    def _enter_sublink_on_website(self, company_name, url):
        def enter_the_link(href):
            return_val = False
            try:
                self.driver.get(f"{url}{href}")
                return_val = True
            except Exception as e:
                # Invalid sublink
                del e
            # Try to enter the sublink in a different way
            if not return_val:
                try:
                    self.driver.get(href)
                    return_val = True
                except Exception as e:
                    # No sublink on the website - restore the previous page
                    self.driver.get(url)
            self._wait_for_page()
            return return_val

        # Collect all links
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        # Print all links in the results
        results = soup.find_all("a")
        if not results:
            print("No results found.")
            return False
        # Create regex pattern from company name (spaces can be replaced with something else on the website)
        pattern = company_name.lower().replace(" ", r".*")
        # Get the links with their text containing the company name
        results = [result for result in results if re.findall(pattern, result.get_text(strip=True).lower())]
        if len(results) == 1:
            href = results[0].get("href")
            return enter_the_link(href)
        elif len(results) > 1:
            # Check if there is some specific word under given sublinks
            for result in results:
                href = result.get("href")
                if href and enter_the_link(href):
                    if self._contains_keywords(self.driver.page_source, self.company_branch_keywords):
                        return True
        else:
            print(f"No matching link found for company: {company_name}")
        # Restore previous page
        self.driver.get(url)
        return False

    def _wait_for_page(self):
        time.sleep(1) # TODO: get rid of it maybe?
        try:
            WebDriverWait(self.driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
        except Exception as e:
            del e

    def compare_results(self, original_results):
        # Convert all elements to lowercase if all of them are not None and add index
        result_list = [(index, (result[1].lower(), result[2].lower())) for index, result in enumerate(original_results) if all(result)]
        if len(result_list) == 1:
            return original_results[result_list[0][0]]
        elif len(result_list) > 1:
            # filter oroginal_results using indexes
            original_results = [original_results[i] for i in [item[0] for item in result_list]]
            result_list = [item[1] for item in result_list]
            # inconsistent_with_indices = [(index, item) for index, item in enumerate(result_list) if item != result_list[0]]
            inconsistent_elements = [item for item in result_list if item != result_list[0]]
            # if there are multiple entries - pick the first source to resolve conflict
            if inconsistent_elements:
                return original_results[0]
            # Check the result that contains lowercase character (as the second letter) in CEO's name
            best_result = next((x for x in original_results if x[2][1].islower()), original_results[0])
            return best_result
        # Return None if there are no elements
        return None
    
    def _contains_keywords(self, content, keywords):
        """
        Checks if the given content contains any of the specified keywords.
        
        Args:
            content (str): The HTML content of the page.
            keywords (list): List of keywords to search for.
        
        Returns:
            bool: True if any keyword is found, False otherwise.
        """
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator=" ").lower()
        return any(keyword in text for keyword in keywords)

    def fetch_nip_from_page(self, page_source):
        """
        Extracts the NIP from the HTML source of a company's page.
        
        Args:
            page_source (str): The HTML source of the company's page.
        
        Returns:
            str: The NIP number if found, None otherwise.
        """
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        found_element = soup.find(string=lambda text: text and "NIP" in text)
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
    
    def fetch_ceo_from_page(self, page_source):
        """
        Extracts the CEO from the HTML source of a company's page.
        
        Args:
            page_source (str): The HTML source of the company's page.
        
        Returns:
            str: The CEO name if found, None otherwise.
        """
        text_name_search_function = re.compile(self.ceo_pattern, re.IGNORECASE)
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Look for a tag containing CEO (adjust selector based on actual structure)
        found_elements = soup.find_all(string=text_name_search_function)
        
        if found_elements:
            for found_element in found_elements:
                # Start from the parent of the found element
                current = found_element.find_parent()
                # Iterate over all parents (maximum 4 times)
                parent_count = 0
                while current and parent_count < 4:
                    # Iterate over all descendants of the current container
                    all_classes = current.find_all(True)
                    for descendant in all_classes:
                        if descendant.name == "p":
                            # Check if the descendant contains text matching the pattern
                            text_match = re.fullmatch(self.ceo_value_pattern, descendant.get_text(strip=True))
                            if text_match:
                                # Return the entire content of the matching element
                                return descendant.get_text(strip=True)
                    # Move up the tree (to the next parent container)
                    try:
                        current = current.find_parent()
                    except Exception as e:
                        del e
                        break
                    parent_count += 1
        return None
    
    def handle_cookies(self):
        """
        Handles the cookie consent popup by clicking "Reject all" or "Odrzuć wszystko".
        """
        try:
            # Wait for the cookie popup to appear and locate the "Reject all" button
            self._wait_for_page()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            button = soup.find(
                lambda tag: tag.name in ["button", "span", "a"]
                and tag.get_text(strip=True)
                and re.search(r"(Odrzuć wszystk|Reject all|Akceptuj wszystkie|Accept all)", tag.get_text(strip=True))
            )
            # Get XPATH
            tag = button
            xpath = "//" + tag.name
            if tag.get('id'):
                xpath += f"[@id='{tag.get('id')}']"
            elif tag.get('class'):
                xpath += f"[contains(@class, '{tag.get('class')[0]}')]"
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            button.click()
        except Exception as e:
            print("No cookie consent popup found or could not click any button:", e)

    def find_company_data(self, company_name):
        """
        Fetches the NIP of a company by searching Google.
        Args:
            company_name (str): The name of the company.
        Returns:
            str: The NIP of the company, or 'Not found' if unavailable.
        """
        results = []
        for url in self.checking_website_urls:
            try:
                self.driver.get(url)
                self.handle_cookies()
                search_box = self.driver.find_element(By.NAME, "q")
                search_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
                search_box.send_keys(company_name)
                search_box.send_keys(Keys.RETURN)
                # Wait until the page is loaded
                self._wait_for_page()
                # Try to enter a subpage and then perform the search
                self._enter_sublink_on_website(company_name, url)
                nip = self.fetch_nip_from_page(self.driver.page_source)
                ceo = self.fetch_ceo_from_page(self.driver.page_source)
                results.append((company_name, nip, ceo))
            except Exception as e:
                print(f"Error fetching NIP for {company_name}: {e}")
        return self.compare_results(results)