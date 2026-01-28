import requests
import tls_client
from lxml import html
import time
import json
from urllib.parse import urljoin
from settings import DOMAIN, HEADER, LISTING_API_URL, CLIENT_IDENTIFIER, logger, fetch_from_mongo, save_to_mongo

class ApiParamsGetter():    


    def __init__(self):
            self.session = tls_client.Session(client_identifier=CLIENT_IDENTIFIER)
            self.logger = logger


    def _find_key_recursive(self,data, target_key):
    # """Yields all values for a specific key in a nested structure."""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    yield value
                else:
                    yield from self._find_key_recursive(value, target_key)
        elif isinstance(data, list):
            for item in data:
                yield from self._find_key_recursive(item, target_key)

        

    def get_api_params(self,view_all_url):
        page_id = None
        category_id = None
        self.logger.info(f"getting api params from {view_all_url}")
        try:
            response = self.session.get(view_all_url,headers=HEADER)
            self.logger.info(f'status code of {view_all_url} is {response.status_code}')
            if response.status_code != 200:
                print(response.text)
            tree = html.fromstring(response.content)
            script = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]
        except Exception as e:
            self.logger.error(f"error change client identifier {e}")
        try:
            if not script:
                self.logger.critical(f"script tag not found check the respose.text ")
            data = json.loads(script)
            page_id_fetch = list(self._find_key_recursive(data,"pageId"))
            category_id_fetch = list(self._find_key_recursive(data,"tagCodes"))
        except Exception as e:
            self.logger.info(f"params fetching failed becuase {e}")
        try:
            page_id = page_id_fetch[0]
            category_id = category_id_fetch[0][0]
        except Exception as e:
            self.logger.error("api params sending failed")
            print(page_id,category_id)
        return page_id,category_id

        
        


class Crawler(ApiParamsGetter):

    def __init__(self):
        super().__init__()
        self.data = fetch_from_mongo("category_links")
        self.list_of_plp_urls = [url["url"] for url in self.data]
        self.logger = logger
        self.list_of_pdp_urls = []
        self.listing_url = LISTING_API_URL
        self.remove_duplicate_pdp_url = set()
        self.links_to_save = dict()


    def crawl(self):

        for i in self.list_of_plp_urls:
            view_all_url = urljoin(DOMAIN,i)
            pageId,categoryId = self.get_api_params(view_all_url)
            if not pageId or not categoryId:
                self.logger.warning(f"Skipping {view_all_url} - IDs not found")
                continue
            
            PARAMS = {
            "pageSource": "PLP",
            "page": 1,
            "sort": "RELEVANCE",
            "pageId": pageId,
            "page-size": "36",
            "categoryId": categoryId,
            "filters": "sale:false||oldSale:false",
            "touchPoint": "DESKTOP",
            "skipStockCheck": "false"
                        }
            try:
                while True:
                    response = self.session.get(self.listing_url,headers=HEADER,params=PARAMS)
                    self.logger.info(f"[INFO] STATUS CODE FOR PAGE NO : {PARAMS["page"]} = {response.status_code}")

                    if response.status_code != 200:
                        self.logger.error("Request blocked or failed")
                        break
                
                    try:
                        data = response.json()
                    except Exception as e:
                        self.logger.error(f"Cookie Expired or {e}")
                    products = data["plpList"]["productList"]

                    if products:
                        self.logger.info(f" Fetching product urls from Page no: {PARAMS['page']} ")
                        count = 0
                        for i in products:
                            url = i.get("url")
                            if url:
                                print(url)
                                self.list_of_pdp_urls.append(url)
                                count += 1
                        self.logger.info(f" Fetched {count} urls from page no {PARAMS["page"]}")
                        print("****************************************************************")
                        time.sleep(3)
                        PARAMS["page"] += 1

                    else:
                        self.logger.info(" No more products Reached last page")
                        break
                self.logger.info(f"successfully fetched {len(self.list_of_pdp_urls)} links")
            except Exception as e:
                self.logger.error("API page loading failed due to no pageId and categoryId")
        
        self.remove_duplicate_pdp_url = set(self.list_of_pdp_urls)
        self.links_to_save = [{"url":url} for url in self.remove_duplicate_pdp_url]
        save_to_mongo(self.links_to_save,"products_links")
