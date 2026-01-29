from matalanme_category_crawler import CategoryCrawler
from settings import logger

class Main():
    def __init__(self):
        self.logger = logger
        self.category_crawler = CategoryCrawler

    def run(self):
        self.logger.info(f"Starting the process")
        self.category_crawler.category_crawl()
        self,logger.info("Category crawling completed")
