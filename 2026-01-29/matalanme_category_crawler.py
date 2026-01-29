import re
from urllib.parse import urljoin
import requests
from settings import HEADER, DOMAIN, logger, save_to_mongo

class CategoryCrawler():
    def __init__(self):
        self.url = DOMAIN
        self.header = HEADER
        self.logger = logger
        self.session = requests.Session()

    def category_crawl(self):

        self.logger.info("Starting the category crawler")

        response = self.session.get(
                url=self.url,
                headers= self.header,
        )
        self.logger.info("{self.url} retuned {respose.status_code}")
        if response.status_code != 200:
            self.logger.info(f"website blocked request ")
        
        html_text = response.text
        """found this regex by inspecting the page source this is how the
        category links in the navbar available in the page source"""
        category_links_fetch = re.findall(r'\\"category_link\\",\\"classes\\":null,\\"content_type\\":\\"parentcat\\",\\"link\\":\\"(.*?)\\"',html_text)

        #extracting only womens category links
        women_category = set()

        for i in category_links_fetch:
            if "women/" in i:
                women_category.add(urljoin(self.url,i))
        
        women_category = [{"url":url} for url in women_category ]
        print(women_category)

        save_to_mongo(women_category,"women_category_links")