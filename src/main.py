from scraper_facade import ScraperFacade
import sys

def Main():
    search_engine = None
    if len(sys.argv) > 1:
        search_engine = sys.argv[1]
    sf = ScraperFacade(search_engine)
    sf.process()

if __name__ == "__main__":
    Main()