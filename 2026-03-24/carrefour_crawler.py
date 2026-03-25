import requests
from parsel import Selector
from urllib.parse import urljoin
import logging
from settings import HEADERS,COOKIES,CLIENT,DOMAIN,MONGO_COLLECTION_URLS
from items import ProductUrls

class Crawler():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_URLS

    def start(self):
        MAX_RETRIES = 3
        page = 1
        api_url = f"https://www.carrefour.be/nl/dranken/softdrinks?p={page}"
        while True:
            for attempt in range(MAX_RETRIES):
                try:
                    response = requests.get(api_url,headers=HEADERS,cookies=COOKIES)
                    if response.status_code == 200:
                        break
                    else:
                        continue
                except Exception as e:
                    logging.warning(f"Retry {attempt+1} failed: {e}")
            else:
        #All retries failed
                logging.warning("PageNumber %d failed after retries with status code %d", page + 1,response.status_code)
                break
            if response.status_code == 200 and response:
                logging.info("page returned status code %d",response.status_code)
                is_next = self.parse_item(response)
                if not is_next:
                    logging.info("-------Pagination completed--------")
                    break
                #pagination
                page += 1
                api_url = f"https://www.carrefour.be/nl/dranken/softdrinks?p={page}"

            else:
                logging.info("page returned status code %d",response.status_code)

                


    def parse_item(self,response):
        sel = Selector(text=response.text)

        #XPATH
        PRODUCT_XPATH = '//div[@class="gtm-event"]'
        UNIQUE_ID_XPATH = './/div[@class="product js-product"]/@data-pid'
        URL_XPATH = './/div[@class="name-wrapper js-product-tile-gtm"]//@href'
        NAME_XPATH = './/div[@class="name-wrapper js-product-tile-gtm"]//span[@class="d-none d-lg-inline desktop-name"]/text()'
        BRAND_XPATH = './/div[@class="brand-wrapper"]/a//text()'
       # PRICE_XPATH = './/div[@class="pricing-wrapper"]//div[@class="price"]/span/span[@class="sales"]/span[@class="value"]//text()'
        PRICE_XPATH = './/div[@class="pricing-wrapper"]//div[@class="price"]/span/span[@class="sales"]/span[@class="value"]/@content'
        PRICE_PER_UNIT_XPATH = './/div[@class="pricing-wrapper"]//div[@class="price-per-unit-wrapper"]//text()'
        IMG_XPATH = './/div[@class="image-wrapper js-product-tile-gtm"]//img//@data-src'


        #EXTRACTION AND CLEANING

        products = sel.xpath(PRODUCT_XPATH)
        if products:
            for prod in products:

                unique_id_fetch = prod.xpath(UNIQUE_ID_XPATH).extract_first()
                unique_id = unique_id_fetch if unique_id_fetch else ""

                name_fetch = prod.xpath(NAME_XPATH).extract_first()
                name = name_fetch if name_fetch else ""


                pdp_url_fetch = prod.xpath(URL_XPATH).extract_first()
                pdp_url = pdp_url_fetch if pdp_url_fetch else ""


                brand_fetch = prod.xpath(BRAND_XPATH).extract_first()
                brand = brand_fetch.replace("\n","").strip() if brand_fetch else ""


                price_fetch = prod.xpath(PRICE_XPATH).extract_first()
                price = price_fetch if price_fetch else ""

                price_per_unit_fetch = prod.xpath(PRICE_PER_UNIT_XPATH).extract_first()
                price_per_unit = price_per_unit_fetch.replace("\n","").strip() if price_per_unit_fetch else ""

                image_fetch = prod.xpath(IMG_XPATH).extract_first()
                image = image_fetch if image_fetch else ""


                item = {}
                item["unique_id"] = unique_id
                item["name"] = name
                item["pdp_url"] = urljoin(DOMAIN,pdp_url) if pdp_url else ""
                item["brand"] = brand
                item["price"] = price
                item["price_per_unit"] = price_per_unit
                item["image_url"] = image

                logging.info(item)

                try:
                    product_item = ProductUrls(**item)
                    product_item.validate()
                    self.mongo_col.insert_one(item)
                    logging.info("---------DATA SAVE SUCCESSFULLY----------")
                except Exception as e:
                    logging.info("SAVE ERROR DUE TO %s",e)
            return True
        else:
            return False






    def close(self):
        self.mongo.close()


crawler = Crawler()
crawler.start()
crawler.close()
