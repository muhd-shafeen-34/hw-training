import requests
from logging import warning,error
from urllib.parse import urljoin
import items
import time
import random
from settings import DOMAIN,API_HEADER,cookies,CRAWLER_API_URL,CLIENT,MONGO_COLLECTION_CATEGORY,requestCookies,MONGO_COLLECTION_URLS,fetch_from_mongo,default_Request_Cookies



class Crawler():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_URLS

    def start(self):
        metas = fetch_from_mongo(MONGO_COLLECTION_CATEGORY,0,"url","type","name","slug")


        for meta in metas:
            params = {
 
			"type": meta.get("type",""),
			"slug": meta.get("slug",""),
            "page": 1
                }
            while True:
                time.sleep(1) #API has rate limiting
                response = requests.get(CRAWLER_API_URL,headers=API_HEADER,params=params,cookies=requestCookies)
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

                name_fetch = product.get("desc","")
                name = name_fetch if name_fetch else ""

                grammage_details_fetch = product.get("w","")
                grammage_details = grammage_details_fetch if grammage_details_fetch else ""

                brand_name_fetch= product.get("brand",{}).get("name","")
                brand_name = brand_name_fetch if brand_name_fetch else ""

                ean_code_fetch = product.get('ean_code',"")
                ean_code = ean_code_fetch if ean_code_fetch else ""

                regular_price_fetch = product.get("pricing",{}).get("discount",{}).get("mrp","")
                regular_price = regular_price_fetch if regular_price_fetch else ""

                selling_price_fetch = product.get("pricing",{}).get("discount",{}).get("prim_price",{}).get("sp","")
                selling_price = selling_price_fetch if selling_price_fetch else ""

                discount_fetch = product.get("pricing",{}).get("discount",{}).get("d_text","")
                discount = discount_fetch if discount_fetch else ""

                rating_fetch = product.get("rating_info",{}).get("avg_rating","")
                rating = rating_fetch if rating_fetch else ""

                review_fetch = product.get("rating_info",{}).get("review_count","")
                if review_fetch:
                    if type(review_fetch) == int:
                        review = str(review_fetch)
                    else:
                        review = review_fetch
                else:
                    review = ""


                image_list = product.get("images",[])
                large_images = [image.get("l","") for image in image_list] if image_list else []
                
                


                item = {}
                item["unique_id"] = id
                item["pdp_url"] = urljoin(DOMAIN,url)
                item["name"] = name
                item["grammage_details"] = grammage_details
                item["regular_price"] = regular_price
                item["selling_price"] = selling_price
                item["discount"] = discount
                item["brand"] = brand_name
                item["ean_code"] = ean_code
                item["rating"] = rating
                item["review"] = review
                item["images"] = large_images
                warning(item)
                try:
                    product_item = items.ProductUrlItem(**item)
                    product_item.validate()
                    #MONGO_COLLECTION_URLS.insert_one(item)
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