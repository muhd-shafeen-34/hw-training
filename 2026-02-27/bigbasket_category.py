import requests
from logging import info,warning,error
from urllib.parse import urljoin
import items
from settings import DOMAIN,API_HEADER,CATEGORY_API_URL,CLIENT,MONGO_COLLECTION_CATEGORY

class CategoryCrawler():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_CATEGORY
        self.category_api_url = CATEGORY_API_URL
        

    def start(self):
        response = requests.get(self.category_api_url,headers=API_HEADER)
        if response.status_code == 200:
            data = response.json()
            target_categories = {"Coffee","Tea"}
            categories = data.get("categories",[])
            try:
                for cat in categories:
                    for child in cat.get("children",[]):
                        name = child.get("name","")
                        if name in target_categories:
                            item = {}
                            item["url"] = urljoin(DOMAIN,child.get("url",""))
                            item["name"] = child.get("name","")
                            item["slug"] = child.get("slug","")
                            item["type"] = child.get("type","")
                            try:
                                cat_item = items.ProductCatUrlItem(**item)
                                cat_item.validate()
                                self.mongo_col.insert_one(item)
                                warning("saved to mongo")
                            except:
                                error('mongo saving error occured on this data due to %s',e)
                            warning(item)
            except Exception as e:
                error("Error occured due to :- %s",e)
        else:
            warning("website returned response status code:- %d",response.status_code)


    def close(self):
        self.mongo.close()


category_crawler = CategoryCrawler()
category_crawler.start()
category_crawler.close()



