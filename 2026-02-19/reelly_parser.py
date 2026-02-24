import requests as rq
import settings
import re
import reelly_items
import time

class Parser():
    def __init__(self):
        self.mongo = settings.client
        self.mongo_col = settings.MONGO_COLLECTION_DATA
        self.logger = settings.logger
    
    def start(self):
        metas = settings.fetch_from_mongo(settings.PDP_URLS_COLLECTION,"api_url")

        for meta in metas:
            url = meta.get("url")
            api_url = meta.get("api_url")
            api_response = rq.get(api_url,headers=settings.api_header)
            if api_response:
                self.parse_item(url,api_response)
                time.sleep(3)
            else:
                self.logger.info("api error")
    


    def parse_item(self,url,api_response):
        p_data = api_response.json()

        unique_id_fetch = p_data["id"]
        unique_id = str(unique_id_fetch) if unique_id_fetch else ""

        url = url
        name_fetch = p_data["name"]
        name = name_fetch if name_fetch else ""

        developer_fetch = p_data["developer"]["name"]
        developer = developer_fetch if developer_fetch else ""

        status_fetch = p_data["status"]
        status = status_fetch if status_fetch else ""

        unit_types_fetch = p_data["unit_types"]
        unit_types = unit_types_fetch if unit_types_fetch else ""

        price_fetch = p_data["min_price"]
        price = str(price_fetch) if price_fetch else ""

        district_fetch = p_data["district"]
        district = district_fetch if district_fetch else ""

        image_url_fetch = p_data["cover_image"]["url"]
        image_url = image_url_fetch if image_url_fetch else ""


        description_fetch = p_data["overview"]
        description = re.sub(r'<[^>]*>|\n|\t|[^a-zA-Z0-9\s.,:-]', ' ', description_fetch).strip() if description_fetch else ""


        item = {}
        item["unique_id"] = unique_id
        item["url"] = url
        item["name"] = name
        item["price"] = price
        item["image_url"] = image_url
        item["status"] = status
        item["developer"] = developer
        item["unit_types"] = unit_types
        item["district"] = district
        item["description"] = description
        self.logger.info(item)
        try:
            product_item = reelly_items.ProductItem(**item)
            product_item.validate()
            self.mongo_col.insert_one(item)
        except Exception as e:
                    self.logger.info("save eroor due to %s",e)
    
    def close(self):
         self.mongo.close()
         


parser = Parser()
parser.start()
parser.close()