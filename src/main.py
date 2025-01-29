from scraper_facade import ScraperFacade
import sys, os

def Main():
    search_engine = None
    load_method = None
    if len(sys.argv) > 2:
        search_engine = sys.argv[1]
        load_method = sys.argv[2]
    sf = ScraperFacade(search_engine, load_method)
    sf.process()

if __name__ == "__main__":
    Main()