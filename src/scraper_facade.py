from website_reader import WebSiteReader
from file_reader_writer import FileReaderWriter

class ScraperFacade:
    def __init__(self):
        """
        Initializes the facade with a list of URLs to scrape.
        """
        self.web_reader = WebSiteReader()
        self.file_writer = FileReaderWriter()

    def process(self):
        """
        Executes the end-to-end scraping process.
        """
        all_companies = []
        urls = self.file_writer.read_from_txt()

        # Step 1: Fetch data from each URL
        for url in urls:
            companies = self.web_reader.fetch_company_data(url)
            all_companies.extend(companies)

        # Step 2: Save results to a CSV file
        self.file_writer.save_to_csv(all_companies)
        print(f"Data saved to {self.file_writer.output_file_name}")

