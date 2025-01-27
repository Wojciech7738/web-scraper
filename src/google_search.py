from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from bs4 import BeautifulSoup

class GoogleSearch:
    def __init__(self):
        # Configure Selenium WebDriver
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    def fetch_nip(self, company_name):
        """
        Fetches the NIP of a company by searching Google.
        Args:
            company_name (str): The name of the company.
        Returns:
            str: The NIP of the company, or 'Not found' if unavailable.
        """
        nip = ""
        try:
            # Open Google
            # self.driver.get("https://www.google.com")
            self.driver.get("https://www.google.com/search?q=NIP+PUPIL+FOODS&sca_esv=2a89619726ebddd5&source=hp&ei=2QaTZ_mzFe2Pxc8PxO-HmA4&iflsig=ACkRmUkAAAAAZ5MU6fUKraYadHvr2DJjE5yGGtsxeERw&ved=0ahUKEwi5hIias42LAxXtR_EDHcT3AeMQ4dUDCBA&uact=5&oq=NIP+PUPIL+FOODS&gs_lp=Egdnd3Mtd2l6Ig9OSVAgUFVQSUwgRk9PRFNIJVAAWCJwAHgAkAEAmAEAoAEAqgEAuAEDyAEA-AEBmAIAoAIAmAMAkgcAoAcA&sclient=gws-wiz&sei=3QaTZ6iYDuSoxc8P3MiLQA")
            # TODO: UNCOMMENT BEGIN
            # self.handle_cookies()
            # search_box = self.driver.find_element(By.NAME, "q")
            # # search_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

            # # Search for the company's NIP
            # query = f"NIP {company_name}"
            # search_box.send_keys(query)
            # time.sleep(1)
            # TODO: UNCOMMENT end
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
            # search_box.send_keys(Keys.RETURN)

            time.sleep(1)

            # TODO: place it somewhere else
            # WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

            # Scrape search results for potential NIP matches
            nip = self._find_nip_in_html()
            # results = self.driver.find_elements(By.CSS_SELECTOR, "span")
            # for result in results:
            #     # Look for a NIP pattern in the text
            #     text = result.text
            #     nip_match = re.search(r"\b\d{3}-\d{2}-\d{2}-\d{2}\b", text)  # Standard NIP format
            #     if nip_match:
            #         return nip_match.group()

        except Exception as e:
            print(f"Error fetching NIP for {company_name}: {e}")
        return nip #TODO: check if there is something checking if "Not found" has been returned.
    
    def _find_nip_in_html(self):
        # Find all <tr> elements on the page
        rows = None
        try:
            rows = self.driver.find_element(By.CSS_SELECTOR, "tr")
        except Exception as e:
            del e
        if not rows:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr"))
                )
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr")
            except Exception as e:
                del e
            if not rows:
                try:
                    rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
                except Exception as e:
                    del e
        for row in rows:
            # Find all <td> elements within the row
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            # Ensure the row contains at least 2 <td> elements to avoid index errors
            if len(cells) >= 2:
                # Extract the text from the second <td> (or adjust index if needed)
                text = cells[1].text

                # Look for a NIP pattern in the text
                nip_match = re.search(r"\b\d{3}-\d{2}-\d{2}-\d{2}\b", text)  # Standard NIP format
                if nip_match:
                    return nip_match.group()
        # Return None if no NIP is found
        return None
    
    def find_company_data(self, company_name):
        nip = self.fetch_nip(company_name)
        ceo = "Jarosław K" #TODO
        return (company_name, nip, ceo)
    
    def close(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()

    def handle_cookies(self):
        """
        Handles the cookie consent popup by clicking "Reject all" or "Odrzuć wszystko".
        """
        try:
            # Wait for the cookie popup to appear and locate the "Reject all" button
            # reject_button = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable(
            #         (
            #             By.XPATH,
            #             "//button[contains(text(), 'Odrzuć wszystko')]"
            #             # "//button[contains(text(), 'Odrzuć wszystko') or contains(text(), 'Reject all')]"
            #         )
            #     )
            # )
            time.sleep(3)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            reject_button = soup.find('button', text=lambda x: x and ('Odrzuć wszystko' in x or 'Reject all' in x))
            # Get XPATH
            tag = reject_button
            xpath = "//" + tag.name
            if tag.get('id'):
                xpath += f"[@id='{tag.get('id')}']"
            elif tag.get('class'):
                xpath += f"[contains(@class, '{tag.get('class')[0]}')]"
            reject_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            reject_button.click()
            print("Clicked 'Reject all' button.")
        except Exception as e:
            print("No cookie consent popup found or could not click the 'Reject all' button:", e)