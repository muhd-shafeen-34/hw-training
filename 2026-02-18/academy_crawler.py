import requests as rq
import parsel as pq
from urllib.parse import urljoin
import settings
from pymongo import MongoClient
import time


class Crawler():
    def __init__(self):
        self.logger = settings.logger

    def start(self):

        
        """here the run script"""

        urls = settings.fetch_from_mongo(settings.CATEGORY_COLLECTION_NAME)
        self.logger.info("category links are fetched successfully")
        self.logger.info("starting the crawler.......")
        for url in urls:
            meta = {}
            meta["category"] = url
            pageno = meta.get("pageno",1)

            api_url = f"{url}?page_{pageno}"
            while True:
                settings.header["Referer"] = url
                response = rq.get(api_url,headers=settings.header)
                self.logger.info("wesite returned status %d",response.status_code)
                self.logger.info("currently fetching %s",response.url)
                is_next = self.parse_item(response)
                if not is_next:
                    self.logger.info("Pagination Completed ")
                    break

                pageno += 1
                api_url = f"{url}?page_{pageno}"
                meta[pageno] = pageno



        
    def parse_item(self,response):
        time.sleep(2)
        html = response.text
        sel = pq.Selector(text=html)

        #XPATHS

        PRODUCTS_XPATH = '//div[@data-auid="ProductCard"]'
        PDP_URL_XPATH = './/a[@data-auid="product-title"]/@href'
        PDP_NAME_XPATH = './/a[@data-auid="product-title"]//text()'
        PDP_RATING_XPATH = './/span[contains(@class,"ratingAvg") and contains(@class,"textCaption")]//text()'
        PDP_REVIEW_COUNT_XPATH = './/a[contains(@class,"ratingCount") and contains(@class,"focusable") and contains(@class,"smallLink")]/text()'


        #EXTRACTION

        products = sel.xpath(PRODUCTS_XPATH)
        if products:
            self.logger.info("products container fetched total %d products",len(products))
            for product in products:
                pdp_url = product.xpath(PDP_URL_XPATH).extract_first()

                pdp_name_fetch = product.xpath(PDP_NAME_XPATH).extract_first().strip()
                pdp_name = pdp_name_fetch if pdp_name_fetch else ""
    
                pdp_rating_fetch = product.xpath(PDP_RATING_XPATH).extract_first()
                pdp_rating = pdp_rating_fetch if pdp_rating_fetch else ""

                pdp_review_count_fetch = product.xpath(PDP_REVIEW_COUNT_XPATH).extract_first().strip("()")
                pdp_review_count = pdp_review_count_fetch if pdp_review_count_fetch else ""

                #item yield

                item = {}
                item["url"] = urljoin(settings.url,pdp_url)
                item["name"] = pdp_name
                item["rating"] = pdp_rating
                item["review"] = pdp_review_count
                self.logger.info(item)
                try:
                    self.save_mongo(item)
                except:
                    pass
            return True
        return False
    


    def save_mongo(self,item):
        if not item:
            print("No data provided to save.")
            return

        try:
            client = MongoClient(settings.MONGO_URI)
            collection = client[settings.DB_NAME][settings.PDP_URLS_COLLECTION_NAME]
            collection.create_index("url", unique=True)
            collection.update_one(
            {"url": item["url"]},   # unique key
            {"$set": item},
            upsert=True
            )
            self.logger.info("pdp details saved successfully")
        except Exception as e:
            self.logger.exception("Mongo save failed due to %s",e)
        


crawler = Crawler()
crawler.start()







# meta = {}
# meta["category"] = url
# pageno = meta.get("pageno",1)

# api_url = f"{url}?page_{pageno}"
# while True:
#     response = rq.get(api_url,headers=settings.header)
#     html = response.text
#     sel = pq.Selector(text=response.text)
#     print(response.status_code)
#     if response.status_code == 200:
#         print(response.url)
#         is_next = products = sel.xpath('//div[@data-auid="ProductCard"]')
#         product = is_next[0]
#         pdp_link = product.xpath('//a[@data-auid="product-title"]/@href').extract_first()
#         pdp_name = product.xpath('//a[@data-auid="product-title"]//text()').extract_first()
#         pdp_rating = product.xpath('//span[contains(@class,"ratingAvg") and contains(@class,"textCaption")]//text()').extract_first()
#         if not is_next:
#             print("pagination completed")
#             break
#         print(len(products))
#         print(pdp_link)
#         print(pdp_name)
#         print(pdp_rating)
#         ageno += 1
#         api_url =p f"{url}?page_{pageno}"
#         meta[pageno] = pageno