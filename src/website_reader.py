import requests
from bs4 import BeautifulSoup
import re

class WebSiteReader:
    def __init__(self):
        pass

    # def fetch_company_data(self, url):
    #     """
    #     Fetches company names and NIP numbers from the given URL.
    #     Args:
    #         url (str): The URL of the page to scrape.
    #     Returns:
    #         list: A list of dictionaries containing company names and NIP numbers.
    #     """
    #     companies = []

    #     try:
    #         # Step 1: Fetch the content of the page
    #         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    #         response.raise_for_status()  # Ensure the request was successful
    #     except requests.exceptions.RequestException as e:
    #         print(f"Failed to fetch data from {url}: {e}")
    #         return companies

    #     # Step 2: Parse HTML content
    #     soup = BeautifulSoup(response.text, 'html.parser')

    #     # Step 3: Extract company information (example structure, may vary)
    #     # Replace 'selector_for_company_name' and 'selector_for_nip' with real CSS selectors
    #     company_elements = soup.select('.company')  # Example class for company data
    #     for company in company_elements:
    #         name = company.select_one('.name').get_text(strip=True)  # Extract company name
    #         nip = company.select_one('.nip').get_text(strip=True)  # Extract NIP number
    #         companies.append({'name': name, 'nip': nip})

    #     return companies

    def fetch_company_data(self, url):
        """
        Fetches company names and NIP numbers from the given URL.
        Args:
            url (str): The URL of the page to scrape.
        Returns:
            list: A list of dictionaries containing company names and NIP numbers.
        """
        companies = []
        url = url.strip()  # Ensure the URL is clean and valid

        try:
            # Step 1: Fetch the content of the page
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Ensure the request was successful
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from {url}: {e}")
            return companies

        # Step 2: Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Look for information on "About Us" or "Contact" pages
        about_info = self.extract_about_us(soup)
        contact_info = self.extract_contact_info(soup)

        # Step 4: Save extracted information
        company_data = {
            "name": about_info.get("name", "Unknown"),
            "nip": contact_info.get("nip", "Unknown")
        }
        companies.append(company_data)

        return companies
    
    def extract_about_us(self, soup):
        """
        Extracts company name or related data from the "About Us" section.
        Args:
            soup (BeautifulSoup): Parsed HTML content.
        Returns:
            dict: A dictionary containing the company name.
        """
        about_info = {}
        about_link = soup.find("a", text=re.compile(r"O.+(nas|NAS)"))
        if about_link:
            about_info = self.parse_subpage(about_link, soup)
        # if about_section:
        #     about_info["name"] = about_section.get_text(strip=True)
        return about_info

    def extract_contact_info(self, soup):
        """
        Extracts contact-related information, such as NIP, from the "Contact" section.
        Args:
            soup (BeautifulSoup): Parsed HTML content.
        Returns:
            dict: A dictionary containing the NIP.
        """
        contact_info = {}
        contact_section = soup.find("section", text=lambda x: x and "Kontakt" in x)
        if contact_section:
            # Try to find NIP (e.g., NIP: 123-456-78-90)
            nip = contact_section.find(text=lambda x: "NIP" in x)
            if nip:
                contact_info["nip"] = nip.split(":")[-1].strip()
        return contact_info
    
    def parse_subpage(self, link, soup):
        page_info = {}
        if link and link.get("href"):
            about_page_url = link["href"]

            # Handle relative URLs
            if not about_page_url.startswith("http"):
                base_url = soup.find("base")["href"] if soup.find("base") else ""
                about_page_url = base_url + about_page_url

            # Fetch and parse the "About Us" page
            try:
                response = requests.get(about_page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                about_soup = BeautifulSoup(response.text, "html.parser")
                about_text = about_soup.get_text(strip=True)
                page_info["name"] = about_text[:200]  # Extract the first 200 characters as a preview
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch 'About Us' page: {e}")
        return page_info


    