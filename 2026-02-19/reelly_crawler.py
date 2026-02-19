import settings
import requests as rq
import parsel as pq
import logging
import reelly_items

class Crawler():
    def __init__(self):
        self.logger = settings.logger
    def start(self):
        response = rq.get(settings.api_url,headers=settings.api_header,params=settings.api_params)

        print(response.status_code)
        print(response.url)
        is_next = self.parse_item(response)
        if not is_next:
            self.logger.info('api error')

        
        
    def parse_item(self,response):
        data = response.json()
        details = data["results"]
        if details:
            for i in details:
                id = i['id']
                name = i["name"]
                item = {}
                item["unique_id"] = str(id)
                item["url"] = f"{settings.start_url}/projects/{id}" if id else "" 
                item["api_url"] = f"{settings.product_api}/{id}" if id else ""
                item["name"] = name
                self.logger.info(item)
                try:
                    product_item = reelly_items.ProductUrl(**item)
                    product_item.validate()
                    settings.PDP_URLS_COLLECTION.insert_one(item)
            
                except Exception as e:
                    self.logger.info("save eroor due to %s",e)
            return True
        return False


crawler = Crawler()
crawler.start()


