from website_reader import WebSiteReader
from file_reader_writer import FileReaderWriter
# from google_search import GoogleSearch
from website_search import WebsiteSearch

class ScraperFacade:
    def __init__(self):
        """
        Initializes the facade with a list of URLs to scrape.
        """
        # self.web_reader = WebSiteReader()
        self.google_searcher = WebsiteSearch()
        self.file_writer = FileReaderWriter()

    def process(self):
        all_companies_info = []
        company_names = self.file_writer.read_from_txt()

        # Step 1: Fetch data from each URL
        for company_name in company_names:
            company_info = self.google_searcher.find_company_data(company_name)
            all_companies_info.extend(company_info)

        # Step 2: Save results to a CSV file
        self.file_writer.save_to_csv(all_companies_info)
        print(f"Data saved to {self.file_writer.output_file_path}")

