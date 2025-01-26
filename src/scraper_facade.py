from website_reader import WebSiteReader
from file_reader_writer import FileReaderWriter
# from google_search import GoogleSearch
from website_search import WebsiteSearch
from functools import wraps

def cleanup(method):
    """
    A decorator to clean up specified attributes of the class instance after the method finishes.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = None
        try:
            result = method(self, *args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # Clean up the specified attributes
            self.google_searcher.close()
        return result
    return wrapper


class ScraperFacade:
    def __init__(self):
        """
        Initializes the facade with a list of URLs to scrape.
        """
        # self.web_reader = WebSiteReader()
        self.google_searcher = WebsiteSearch()
        self.file_writer = FileReaderWriter()

    @cleanup
    def process(self):
        all_companies_info = []
        company_names = self.file_writer.read_from_txt()

        # Step 1: Fetch data from each URL
        for company_name in company_names:
            company_info = self.google_searcher.find_company_data(company_name)
            if company_info: # TODO: solve "not found" conflict
                all_companies_info.append(company_info)
        # Step 2: Save results to a CSV file
        self.file_writer.save_to_csv(all_companies_info)
        print(f"Data saved to {self.file_writer.output_file_path}")

