import requests

class GUSAPIClient:
    def __init__(self, api_key):
        self.api_url = "https://dane.biznes.gov.pl/api/ceidg/v2/firmy?query"
        self.api_key = api_key
        
    def format_company_name(self, company_name):
        """
        Format the company name into the required query parameter format.
        Example: "PUPIL FOODS" -> "nazwa=pupil&nazwa=foods"
        """
        words = company_name.split()
        formatted_name = "&".join([f"nazwa={word.lower()}" for word in words])
        return formatted_name

    def find_company_data(self, company_name):
        """Search for a company by its name and return its NIP, owner's first name, and last name."""
        formatted_name = self.format_company_name(company_name)
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        params = {
            "nazwa": formatted_name,  # Query parameter for company name
            "limit": 1              # Limit results to 1 for simplicity
        }

        # query_url = f"{self.api_url}&{formatted_name}"
        query_url = f"{self.api_url}"
        
        try:
            response = requests.get(query_url, headers=headers, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            
            try:
                data = response.json()
            except ValueError:
                print("Response is not in JSON format. Raw response:")
                print(response.text)
                return None
            companies = data.get("firmy", [])
            if companies:
                company = companies[0]
                owner = company.get("wlasciciel", {})
                return (company.get("nazwa"), owner.get("nip"), owner.get("imie") + " " + owner.get("nazwisko"))
            else:
                print("No company found with the specified name.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

