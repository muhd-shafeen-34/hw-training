import requests
from parsel import Selector
from urllib.parse import urljoin
import logging
import items
from settings import HEADER,START_URL,DOMAIN,CLIENT,MONGO_COLLECTION_URLS

class Crawler():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_URLS
    def start(self):
        pageno = 1
        url = f"{START_URL}?page={pageno}"
        while True:
            response = requests.get(url,headers=HEADER)
            if response.status_code == 200:
                logging.warning("%s returned status code %d",url,response.status_code)
                is_next = self.parse_item(response)
                if not is_next:
                    logging.warning("pagination completed")
                    break
                pageno += 1
                url = f"{START_URL}?page={pageno}"
            else:
                logging("%s returned status code %d",url,response.status_code)

    def parse_item(self,response):
        html = response.text
        sel = Selector(text=html)

        ##### X P A T H #####

        PRODUCT_CARDS = '//div[contains(@class,"product-item product-item--vertical   1/3--tablet-and-up 1/4--desk")]'
        CRAWLER_PRODUCT_LINK = './/a[contains(@class,"product-item__title text--strong link")]/@href'
        CRAWLER_PDP_NAME_XPATH = './/a[contains(@class,"product-item__title text--strong link")]//text()'
        CRAWLER_PDP_PRICE_XPATH = './/div[contains(@class,"product-item__price-list price-list")]/span/text()[2]'
        CRAWLER_PDP_MANUFACTURER = './/a[contains(@class,"product-item__vendor link")]/text()'

        products = sel.xpath(PRODUCT_CARDS)
        if products:
            for product in products:
                pdp_url = product.xpath(CRAWLER_PRODUCT_LINK).extract_first()
                pdp_name = product.xpath(CRAWLER_PDP_NAME_XPATH).extract_first()
                pdp_price = product.xpath(CRAWLER_PDP_PRICE_XPATH).extract_first()
                pdp_manufacturer = product.xpath(CRAWLER_PDP_MANUFACTURER).extract_first()


                item = {}
                item["pdp_url"] = urljoin(DOMAIN,pdp_url)
                item["pdp_name"] = pdp_name
                item["pdp_price"] = pdp_price
                item["pdp_manufacturer"] = pdp_manufacturer

                logging.warning(item)

                try:
                    product_item = items.ProductUrls(**item)
                    product_item.validate()
                    self.mongo_col.insert_one(item)
                except Exception as e:
                    logging.warning("save error due to %s ",e)

            
            return True

        return False

        
    def close(self):
        self.mongo.close()

crawler = Crawler()
crawler.start()
crawler.close()
