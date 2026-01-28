from handm_crawler import Crawler
from handm_parser import Parser
from handm_category_crawler import CategoryCrawler
from lxml import html
from settings import DOMAIN, save_to_csv, save_to_mongo, fetch_from_mongo, logger
import tqdm as progress
import time

class Main():
    def __init__(self):
        
        self.pdp_data = []
        self.logger = logger
    
    def start(self):

        self.category = CategoryCrawler()

        self.logger.info("startitng category crawling.....")
        self.category.category_crawl()

        self.crawler = Crawler()
        self.logger.info("[INFO] Starting the Crawling Process ")

        self.crawler.crawl()

        parser = Parser()
        self.data = fetch_from_mongo("products_links_two",limit=200)
        self.pdp_urls = [url["url"] for url in self.data]
        print(len(self.pdp_urls))

        for i in progress.tqdm(self.pdp_urls,desc ="Extracting.............."):
            try:
                data = parser.parser(i)
                print(f"[INFO] Data from link {DOMAIN}{i} printing")
                print(data)
                self.pdp_data.append(data)
            except Exception as e:
                print(f"[ERROR] Failed to parse {DOMAIN}{i}")
                print(f"[ERROR] Reason: {e}")
                continue
            
        save_to_csv(self.pdp_data)
        save_to_mongo(self.pdp_data,"products_data")

        

if __name__ == "__main__":
    runner = Main()
    runner.start()

