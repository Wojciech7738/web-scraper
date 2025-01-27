from website_search import WebsiteSearch
from file_reader_writer import FileReaderWriter
from functools import wraps
from gus_api import GUSAPIClient
from article_read import ArticleReader

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
            try:
                # Clean up the specified attributes
                self.dedicated_searcher.close()
            except Exception as e:
                del e
        return result
    return wrapper


class ScraperFacade:
    def __init__(self, search_engine="default"):
        """
        Initializes the facade with a list of URLs to scrape.
        """
        self.file_writer = FileReaderWriter()
        self.dedicated_searcher = None
        self.gus_client = None
        if search_engine == "API":
            self.perform_search = self.gus_api_search
        else:
            self.perform_search = self.dedicated_website_search

    def search_company_info(self, search_engine):
        all_companies_info = []
        # company_names = self.file_writer.read_from_txt()
        company_names = ArticleReader().read_companies()
        for company_name in company_names:
            company_info = search_engine.find_company_data(company_name)
            if company_info:
                all_companies_info.append(company_info)
        # Step 2: Save results to a CSV file
        self.file_writer.save_to_csv(all_companies_info)
        print(f"Data saved to {self.file_writer.output_file_path}")

    @cleanup
    def dedicated_website_search(self):
        self.dedicated_searcher = WebsiteSearch()
        self.search_company_info(self.dedicated_searcher)

    def gus_api_search(self):
        key = self.file_writer.read_from_txt(get_api_key=True)
        if key:
            self.gus_client = GUSAPIClient(key[0])
            self.search_company_info(self.gus_client)
        else:
            print("Cannot find API key. Make sure it is placed in input/api_key.txt file.")

    def process(self):
        self.perform_search()

