from crawler import Crawler
from parser import Parser
from settings import DOMAIN, PARAMS, save_to_csv, save_to_mongo
import tqdm as progress
import time

class Main():
    def __init__(self):
        self.pdp_data = []
    
    def start(self):
        crawler = Crawler()
        parser = Parser()

        print("[INFO] Starting the Crawling Process ")
        pdp_urls = crawler.crawl()

        print(len(pdp_urls))

        for i in progress.tqdm(pdp_urls,desc ="Extracting.............."):
            try:
                data = parser.parser(i)
                print(f"[INFO] Data from link {DOMAIN}+{i} printing")
                print(data)
                self.pdp_data.append(data)
            except Exception as e:
                print(f"[ERROR] Failed to parse {DOMAIN}{i}")
                print(f"[ERROR] Reason: {e}")
                continue
        save_to_csv(self.pdp_data)
        save_to_mongo(self.pdp_data)

        

if __name__ == "__main__":
    runner = Main()
    runner.start()

