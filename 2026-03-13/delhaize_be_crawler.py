import requests
from settings import DOMAIN,API_HEADER,API,CLIENT,MONGO_COLLECTION_URLS
import json
import logging
from items import ProductUrls
from urllib.parse import urljoin


class Crawler():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_URLS
    
    def start(self):

        #parameters of the api which needs to change according to pagination
        variables = {
                "lang": "nl",
                "searchQuery": "",
                "category": "v2DRISOF",
                "pageNumber": 0,
                "pageSize": 20,
                "filterFlag": True,
                "fields": "PRODUCT_TILE",
                "plainChildCategories": True
            }

        extensions = {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "6207aa07553962b9956d475b63737d2b03b3eb7b7e6fa6ffbfc709f9894c5bdd"
                }
            }
        MAX_RETRIES = 3
        #pagination incrementing variable
        page = 0
        #loop for pagination
        while True:
            for attempt in range(MAX_RETRIES):
                try:
                    variables["pageNumber"] = page

                    api_params = {
                        "operationName": "GetCategoryProductSearch",
                        #used json dumbs becuase we need these 2 dict here as a string
                        "variables": json.dumps(variables),
                        "extensions": json.dumps(extensions)
                        }
                    response = requests.get(API,headers=API_HEADER,params=api_params,timeout=10)
                    logging.info("PageNumber %d returned %s",page+1,response.status_code)
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
            if response.status_code == 200:
                is_next = self.parse_item(response) if response else ""
                if not is_next:
                    logging.info("----------PAGINATION ENDED----------")
                    break

                page += 1
            else:
                logging.info("PageNumber %d returned %s",page+1,response.status_code)
                break
            logging.info("--------CRAWLING COMPLETED--------------")

    def parse_item(self,response):
        res = response.json()
        data = res.get("data",{})
        details = data.get("categoryProductSearch",{})
        products = details.get("products",[])
        if products:
            for product in products:
                unique_id = product.get("code","")
                name = product.get("name","")
                brand = product.get("manufacturerName","")
                url = product.get("url","")

                grammage_details_fetch = product.get("price",{})
                grammage_details = grammage_details_fetch.get("supplementaryPriceLabel2","") if grammage_details_fetch else ""

                price_fetch = grammage_details_fetch.get("unitPrice","")
                price = float(price_fetch) if price_fetch else ""
                unit_price = grammage_details_fetch.get("supplementaryPriceLabel1","")


                availability = product.get("stock",{})
                instock = str(availability.get("inStock","")) if availability else ""
                rating = str(product.get("averageRating",""))
                review = str(product.get("numberOfReviews",""))
                country = product.get("country","")

                promotion_details = product.get("potentialPromotions",[])
                promotion_description,promo_end_date,promo_start_date = [],[],[]
                if promotion_details:
                    for promo in promotion_details:
                        promotion_description.append(promo.get("description",""))
                        promo_start_date.append(promo.get("startDate",""))
                        promo_end_date.append(promo.get("endDate",""))
                

                image_urls_fetch = product.get("images",[])
                image_url = ""
                if image_urls_fetch:
                    for img_url in image_urls_fetch:
                        if img_url["format"] == "xlarge":
                            image_url = img_url.get("url","")
                

                item = {}
                item["unique_id"] = unique_id
                item["name"] = name
                item["brand"] = brand
                item["pdp_url"] = urljoin(DOMAIN,url)
                item["grammage_details"] = grammage_details
                item["price"] = price
                item["unit_price"] = unit_price
                item["image_url"] = image_url
                item["rating"] = rating
                item["review"] = review
                item["promotion_description"] = promotion_description
                item["promotion_startDate"] = promo_start_date
                item["promotion_endDate"] = promo_end_date
                item["instock"] = instock
                item["country"] = country
                logging.info("----PRODUCT DETAILS------------")
                logging.info(item)

                try:
                    product_item = ProductUrls(**item)
                    product_item.validate()
                    self.mongo_col.insert_one(item)
                    logging.info("-------DATA SAVED SUCCESSFULLY---------")
                except Exception as e:
                    logging.info("------------ SAVE ERROR ------DUE TO -----\n")
                    logging.info(e)

            return True
        else:
            return False



                  
            
    def close(self):
        self.mongo.close()

crawler = Crawler()
crawler.start()
crawler.close()
