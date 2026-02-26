import requests
from logging import warning,error
from urllib.parse import urljoin
import items
import time
import random
from settings import DOMAIN,API_HEADER,CRAWLER_API_URL,CLIENT,MONGO_COLLECTION_CATEGORY,MONGO_COLLECTION_URLS,fetch_from_mongo,list_of_agents



class Crawler():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_URLS

    def start(self):
        metas = fetch_from_mongo(MONGO_COLLECTION_CATEGORY,"url","type","name","slug")


        for meta in metas:
            params = {
 
			"type": meta.get("type",""),
			"slug": meta.get("slug",""),
            "page": 1
                }
            while True:
                time.sleep(10)
                #API_HEADER["User-Agent"] = random.choice(list_of_agents)
                response = requests.get(CRAWLER_API_URL,headers=API_HEADER,params=params)
                if response.status_code == 200:
                    warning(f"type = {params['slug']} status = {response.status_code} page number = {params["page"]}")
                    next = self.parse_item(response)
                    if not next:
                        warning("pagination ended")
                        break
                    params["page"] += 1
                elif response.status_code != 200:
                    warning(f"type = {params['slug']} status = {response.status_code} page number = {params["page"]}")
                    break
                    
                else:
                    continue
            
    

    def parse_item(self,response):
        data = response.json()
        products = data["tabs"][0]["product_info"]["products"]
        if products:
            for product in products:
                id = product.get("id","")
                url = product.get("absolute_url","")
                name = product.get("desc","")
                grammage_details = product.get("w","")
                brand_name= product.get("brand",{}).get("name","")
                ean_code = product.get('ean_code',"")
                regular_price = product.get("pricing",{}).get("discount",{}).get("mrp","")
                selling_price = product.get("pricing",{}).get("discount",{}).get("prim_price",{}).get("sp","")
                image_list = product.get("images",[])
                if image_list:
                    large_images = [image.get("l","") for image in image_list]
                else:
                    large_images = ""
                


                item = {}
                item["unique_id"] = id
                item["pdp_url"] = urljoin(DOMAIN,url)
                item["name"] = name
                item["grammage_details"] = grammage_details
                item["regular_price"] = regular_price
                item["selling_price"] = selling_price
                item["brand"] = brand_name
                item["ean_code"] = ean_code
                item["images"] = large_images
                warning(item)
                try:
                    product_item = items.ProductUrlItem(**item)
                    product_item.validate()
                    MONGO_COLLECTION_URLS.insert_one(item)
                    warning("----DATA SAVED SUCCESSFULLY-------")
                except Exception as e:
                    warning("save error occured due to %s ",e)
            return True
        return False
    
    def close(self):
        self.mongo.close()

    

crawler = Crawler()
crawler.start()
crawler.close()















# while True:
#     response = requests.get(CRAWLER_API_URL,headers=API_HEADER)
#     params = {
 
# 			"type": "pc",
# 			"slug": "coffee", #change this into tea for next url
# 			"page": 1
# }


#     print(respponse.status_code)
#     if respponse.status_code != 200:
#         break
#     data = respponse.json()
#     products = data["tabs"][0]["product_info"]["products"]
#     for pdp in products:
#         link = pdp["absolute_url"]
#         id =pdp["id"]
#         item = {}
#         item[link] = link
#         item[id] = id
#     params["page"] += 1