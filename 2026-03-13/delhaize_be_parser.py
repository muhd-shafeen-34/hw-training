import requests
import json
import logging
import re
import items
from datetime import date
from parsel import Selector
from urllib.parse import urljoin
from settings import DOMAIN,API,API_HEADER,PDP_HEADER,CLIENT,MONGO_COLLECTION_URLS,MONGO_COLLECTION_DATA,fetch_from_mongo

class Parser():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_DATA
    
    def start(self):
        metas = fetch_from_mongo(MONGO_COLLECTION_URLS,0)
        logging.warning("total %d products to parser",len(metas))
        logging.warning("--- S T A R T I N G  P A R S E R-----")

        for meta in metas:
            
            crawler_unique_id = meta.get("unique_id","")
            crawler_pdp_url = meta.get("pdp_url","")
            crawler_grammage_details = meta.get("grammage_details","")
            crawler_brand = meta.get("brand","")
            crawler_price = meta.get("price","")
            crawler_price_per_unit = meta.get("unit_price","")
            crawler_instock = meta.get("instock","")
            crawler_image = meta.get("image_url","")
            variables = {
                        "productCode":crawler_unique_id,
                        "lang" : "nl"
                        }

            pdp_api_params = {
                        "operationName": "ProductDetails",
                        "variables": json.dumps(variables),
                        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"bc98c7e3bfdca594d65bbaebb539e81887459c27c39e860f5538f05739f16236"}}'
                        }
            pdp_response = requests.get(crawler_pdp_url,headers=PDP_HEADER)
            api_response = requests.get(API,headers=API_HEADER,params=pdp_api_params)

            if pdp_response.status_code == 200 and api_response.status_code == 200:
                logging.warning("webpage and api of %s returned %d",crawler_pdp_url,200)
                self.parse_item(pdp_response,api_response,crawler_unique_id,crawler_brand,crawler_grammage_details,crawler_price,crawler_price_per_unit,crawler_pdp_url,crawler_instock,crawler_image)
            else:
                logging.warning("%s page source returned %d and api returned %d",crawler_pdp_url,pdp_response.status_code,api_response.status_code)
            logging.warning("---- P A R S E R ------ C O M P L E T E D --------")




    def parse_item(self,pdp_response,api_response,crawler_unique_id,crawler_brand,crawler_grammage_details,crawler_price,crawler_price_per_unit,crawler_pdp_url,crawler_instock,crawler_image):

        sel = Selector(text=pdp_response.text)
        results = api_response.json()
        data = results["data"]
        product = data.get("productDetails","")


        #XPATH

        PRODUCT_NAME_XPATH = '//h1[@data-testid="product-common-header-title"]/text()'
        BREADCRUMB_XPATH = '//nav[@aria-label]//text()'

        # FIELD EXTRACTION AND CLEANING
        unique_id = product.get("code",crawler_unique_id)
        competitor_name = "delhaize"
        extraction_date = date.today().isoformat()

        brand = product.get("manufacturerName",crawler_brand)

        grammage_details_fetch = product.get("price",{})
        grammage_details = grammage_details_fetch.get("supplementaryPriceLabel2",crawler_grammage_details)

        grammage_regex = re.search(r'(\d+(?:\.\d+)?)\s*(ml|cl|l)\b', grammage_details, re.I)
        grammage_quantity = grammage_regex.group(1) if grammage_regex else ""
        grammage_unit = grammage_regex.group(2) if grammage_regex else ""

        product_name_fetch = sel.xpath(PRODUCT_NAME_XPATH).extract_first()
        product_name = f"{product_name_fetch}{grammage_details}" if product_name_fetch else ""

        breadcrumbs_pdp_fetch = sel.xpath(BREADCRUMB_XPATH).extract()
        breadcrumbs_pdp = list(dict.fromkeys(breadcrumbs_pdp_fetch))
        breadcrumb_api = product.get("categories",[])
        breadcrub_list = []
        for bread in breadcrumb_api:
            breadcrub_list.insert(0,bread.get("name",""))
        
        breadcrumb = [breadcrumbs_pdp[0]] + breadcrub_list + [breadcrumbs_pdp[1]]

        producthierarchy_level1 = breadcrumb[0] if len(breadcrumb) > 0 else ""
        producthierarchy_level2 = breadcrumb[1] if len(breadcrumb) > 1 else ""
        producthierarchy_level3 = breadcrumb[2] if len(breadcrumb) > 2 else ""
        producthierarchy_level4 = breadcrumb[3] if len(breadcrumb) > 3 else ""
        producthierarchy_level5 = breadcrumb[4] if len(breadcrumb) > 4 else ""
        producthierarchy_level6 = breadcrumb[5] if len(breadcrumb) > 5 else ""
        

        regular_price_fetch = product.get("price",{})
        regular_price = regular_price_fetch.get("unitPrice",crawler_price) 
        selling_price = regular_price if regular_price else ""
        price_per_unit = regular_price_fetch.get("supplementaryPriceLabel1",crawler_price_per_unit)


        pdp_url = pdp_response.url if pdp_response.url else crawler_pdp_url

        product_description_fetch = product.get("description","")
        product_description = product_description_fetch if product_description_fetch else ""

        
        nutritional_information = []
        ingredients = ""
        allergens = []
        storage_instructions = ""
        manufacturer_details = ""
        net_content = ""
        special_information = ""
        instruction_for_use = ""
        
        product_details = product.get("wsNutriFactData",{})

        ingredients_fetch = product_details.get("ingredients","")
        ingredients = ingredients_fetch if ingredients_fetch else ""

        nutritional_information_fetch = product_details.get("nutrients",[])
        for nutrients in nutritional_information_fetch:
            nutritional_information = nutrients.get("nutrients",[])
        
        allergens_fetch = product_details.get("allegery",[])
        allergens = allergens_fetch if allergens_fetch else ""

        other_info = product_details.get("otherInfo",[])
        for info in other_info:
            if info.get("key","") == "Bijzondere bewaarvoorschriften":
                storage_instructions  = info.get("value","")
            elif info.get("key","") == "Producent informatie":
                manufacturer_details = info.get("value","")
            elif info.get("key","") == "Andere informatie":
                special_information = info.get("value","")
            elif info.get("key","") == "Net inhoud":
                net_content = info.get("value","")
            elif info.get("key","") == "Bijzondere gebruiksvoorwaarden":
                instruction_for_use = info.get("value","")
        

        site_shown_uom = grammage_details

        competitor_product_key_fetch = product.get("hopeId","")
        competitor_product_key = competitor_product_key_fetch if competitor_product_key_fetch else ""

        instock_fetch = product.get("stock",{})
        instock = str(instock_fetch.get("inStock",crawler_instock))

        product_unique_key = f"{unique_id}P"

        images_fetch = product.get("images",[])
        image_urls = []
        for img in images_fetch:
            if img.get("format","") == "xlarge":
                image_urls.append(urljoin(DOMAIN,img.get("url",crawler_image)))
        
        promotion_description = ""
        promotion_start_date = ""
        promotion_end_date = ""
        promotion_details = product.get("potentialPromotions",[])
        for promo in promotion_details:
            if promo.get("code","") == "BE11742250":
                promotion_description = f"{promo.get("simplePromotionMessage","")} Online"
                promotion_start_date = promo.get("fromDate","")
                promotion_end_date = promo.get("toDate","")

            else:
                promotion_description = promo.get("description","")
                promotion_start_date = promo.get("fromDate","")
                promotion_end_date = promo.get("toDate","")
        

        item = {}
        item["unique_id"] = unique_id
        item["competitor_name"] = competitor_name
        item["extraction_date"] = extraction_date
        item["brand"] = brand
        item["grammage_quantity"] = grammage_quantity
        item["grammage_unit"] = grammage_unit
        item["product_name"] = product_name
        item["breadcrumb"] = breadcrumb
        item["producthierarchy_level1"] = producthierarchy_level1
        item["producthierarchy_level2"] = producthierarchy_level2
        item["producthierarchy_level3"] = producthierarchy_level3
        item["producthierarchy_level4"] = producthierarchy_level4
        item["producthierarchy_level5"] = producthierarchy_level5
        item["producthierarchy_level6"] = producthierarchy_level6
        item["regular_price"] = regular_price
        item["selling_price"] = selling_price
        item["price_per_unit"] = price_per_unit
        item["pdp_url"] = pdp_url
        item["product_description"] = product_description
        item["nutritional_information"] = nutritional_information
        item["ingredients"] = ingredients
        item["allergens"] = allergens
        item["storage_instructions"] = storage_instructions
        item["manufacturer_details"] = manufacturer_details
        item["net_content"] = net_content
        item["special_information"] = special_information
        item["instruction_for_use"] = instruction_for_use
        item["site_shown_uom"] = site_shown_uom
        item["competitor_product_key"] = competitor_product_key
        item["instock"] = instock
        item["product_unique_key"] =  product_unique_key
        item["image_url"] = image_urls
        item["promotion_description"] = promotion_description
        item["promotion_start_date"] = promotion_start_date
        item["promotion_end_date"] = promotion_end_date
        
        logging.warning(item)

        # Validation and database integration
        try:
            product_item = items.ProductItems(**item)
            product_item.validate()
            self.mongo_col.insert_one(item)
            logging.warning("-----DATA SAVED---------")
        except Exception as e:
            logging.warning("------------SAVE-------ERROR--------")
            logging.warning(e)
                    

    def close(self):
        self.mongo.close()

parser = Parser()
parser.start()
parser.close()

