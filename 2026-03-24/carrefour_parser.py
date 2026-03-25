import requests
import json
import re
from items import ProductItems
from parsel import Selector
from datetime import date
import logging
from settings import HEADERS,COOKIES,CLIENT,MONGO_COLLECTION_DATA,MONGO_COLLECTION_URLS,fetch_from_mongo
from playwright_code import get_cookie

class Parser():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_DATA
    def start(self):
        MAX_RETRIES = 3
        logging.info("---PARSER STARTED -----")
        metas = fetch_from_mongo(MONGO_COLLECTION_URLS,0)
        logging.info("--DATA FETCHED FROM DATABASE----")
        # play = get_cookie()
        # COOKIES["cf_clearance"] = play[1]
      #  logging.info("---COOKIE FETCHED -----")
        for meta in metas:
            pdp_url = meta.get("pdp_url","")
            unique_id = meta.get("unique_id","")
            if self.mongo_col.find_one({"unique_id": unique_id}):
                logging.info(f"Skipped: {pdp_url}")
                continue
            for attempt in range(MAX_RETRIES):
                try:
                    response = requests.get(pdp_url,headers=HEADERS,cookies=COOKIES)
                    if response.status_code == 200:
                        break
                    else:
                        continue
                except Exception as e:
                    logging.warning(f"Retry {attempt+1} failed: {e}")
            else:
                logging.warning("Page %s failed after retries with status code %d",pdp_url,response.status_code)
                break

            if response.status_code == 200 and response:
                logging.warning("%s website returned %d status code",pdp_url,response.status_code)
                self.parse_item(response,meta)
            else:
                logging.warning("%s website returned %d status code",pdp_url,response.status_code)
        logging.info("PARSER---COMPLETED--")

    def parse_item(self,response,meta):
        html = response.text
        sel = Selector(text=html)

        #xpath
        PRODUCT_NAME_XPATH = '//h1[@class="product-name"]/text()'
        BRAND_XPATH = '//div[@class="grouping-brand-name-badge"]/div[@class="brand-wrapper"]/div/text()'
        REGULAR_PRICE_XPATH = '//div[@class="grid-container sticky-grid"]//div[@class="price"]//text()'
        PROMOTION_DESCRIPTION_XPATH = '//div[@class="tags-wrapper"]//span[@class="promo-tag-text"]/text()'
        PRICE_PER_UNIT_XPATH = '//div[@class="grid-container sticky-grid"]//div[@class="price-per-unit-wrapper"]//text()'
        BREADCRUMB_XPATH = '//div[@class="desktop-breadcrumb"]/div[contains(@class,"breadcrumb__item")]//text()'
        PRODUCT_DESCRIPTION_XPATH = '//div[contains(@class,"attribute-meer-details")]//text()'
        STORAGE_INSTRUCTIONS_XPATH = '//div[contains(@class,"attribute-houdbaarheid")]//text()'
        INSTRUCTIONSFORUSE_XPATH = '//div[contains(@class,"attribute-bereiding-en-gebruik")]//text()'
        COUNTRY_OF_ORIGIN_XPATH = '//div[contains(@class,"attribute-land-van-herkomst")]//text()'
        ALLERGENS_XPATH = '//div[@class="attribute attribute-bevat  "]//text()'
        IMAGE_URL_XPATH = '//div[@class="grid-container sticky-grid"]//div[@class="image-wrapper"]//div[@class="primary-images col-12"]//@src'
        NUTRITIONAL_INFORMATION_XPATH = '//div[contains(@class,"attribute-voedingswaardetabel")]'
        SPECIAL_INFORMATION_XPATH = '//div[contains(@class,"attribute-lifestyle")]//text()'
        FOOD_PRESERVATION_XPATH = '//div[contains(@class,"attribute-bewaring")]//text()'
        MANUFACTURER_ADDRESS_XPATH = '//div[contains(@class,"attribute-leveranciersadres")]//text()'
        INGREDIENTS_XPATH = '//div[contains(@class,"attribute-ingrediënten")]//text()'
        INSTOCK_XPATH = '//meta[@class="js-pdp-analytics"]//@content'



        unique_id = meta.get("unique_id","")
        competitor_name = "correfour"
        extraction_date = date.today().isoformat()


        product_name_fetch = sel.xpath(PRODUCT_NAME_XPATH).extract_first()
        product_name = product_name_fetch.strip() if product_name_fetch else meta.get("name","")

        brand_fetch = sel.xpath(BRAND_XPATH).extract_first()
        brand = brand_fetch.replace("\n","").replace("No Brand","").strip() if brand_fetch else meta.get("brand","")

        grammage_regex = re.search(r'((?:\d+\s*x\s*)?\d+(?:[.,]\d+)?)\s*(ml|cl|l)\b',product_name,re.I)
        grammage_quantity = grammage_regex.group(1) if grammage_regex else ""
        grammage_unit = grammage_regex.group(2) if grammage_regex else ""

        regular_price_fetch = sel.xpath(REGULAR_PRICE_XPATH).extract()
        regular_price = "".join(regular_price_fetch).replace("\n","").strip() if regular_price_fetch else ""
        selling_price = regular_price if regular_price else ""

        promotion_description_fetch = sel.xpath(PROMOTION_DESCRIPTION_XPATH).extract()
        promotion_description = "".join(promotion_description_fetch) if promotion_description_fetch else ""

        price_per_unit_fetch = sel.xpath(PRICE_PER_UNIT_XPATH).extract_first()
        price_per_unit = price_per_unit_fetch.replace("\n","").strip() if price_per_unit_fetch else ""

        currency = "EUR"
        
        breadcrumb_fetch = sel.xpath(BREADCRUMB_XPATH).extract()
        breadcrumb_list = [ re.sub(r"\s+", " ", x).strip() for x in breadcrumb_fetch if x.strip()] if breadcrumb_fetch else []
        breadcrumb = " > ".join(breadcrumb_list).replace("\n","").strip() if breadcrumb_list else ""

        producthierarchy_level1 = breadcrumb_list[0] if len(breadcrumb_list) > 0 else ""
        producthierarchy_level2 = breadcrumb_list[1] if len(breadcrumb_list) > 1 else ""
        producthierarchy_level3 = breadcrumb_list[2] if len(breadcrumb_list) > 2 else ""
        producthierarchy_level4 = breadcrumb_list[3] if len(breadcrumb_list) > 3 else ""
        producthierarchy_level5 = breadcrumb_list[4] if len(breadcrumb_list) > 4 else ""
        producthierarchy_level6 = breadcrumb_list[5] if len(breadcrumb_list) > 5 else ""

        pdp_url = meta.get("pdp_url","")

        product_description_fetch = sel.xpath(PRODUCT_DESCRIPTION_XPATH).extract()
        product_description = "".join(product_description_fetch).replace("\n","").replace("Meer details","").strip() if product_description_fetch else ""

        storage_instructions_fetch = sel.xpath(STORAGE_INSTRUCTIONS_XPATH).extract()
        storage_instructions = "".join(storage_instructions_fetch).replace("\n","").replace("Houdbaarheid","").strip() if storage_instructions_fetch else ""

        instructionforuse_fetch = sel.xpath(INSTRUCTIONSFORUSE_XPATH).extract()
        instructionforuse = "".join(instructionforuse_fetch).replace("\n","").replace("Bereiding en gebruik","").strip() if instructionforuse_fetch else ""

        allergens_fetch = sel.xpath(ALLERGENS_XPATH).extract()
        allergens = "".join(allergens_fetch).replace("\n","").replace("Bevat","").strip() if allergens_fetch else ""

        country_of_origin_fetch = sel.xpath(COUNTRY_OF_ORIGIN_XPATH).extract()
        country_of_origin = "".join(country_of_origin_fetch).replace("\n","").replace("Land van herkomst","").strip() if country_of_origin_fetch else ""

        images_fetch = sel.xpath(IMAGE_URL_XPATH).extract()
        image_list = list(dict.fromkeys(images_fetch))
        image_url_1 = image_list[0] if len(image_list) > 0 else ""
        image_url_2 = image_list[1] if len(image_list) > 1 else ""
        image_url_3 = image_list[2] if len(image_list) > 2 else ""
        image_url_4 = image_list[3] if len(image_list) > 3 else ""
        image_url_5 = image_list[4] if len(image_list) > 4 else ""
        image_url_6 = image_list[5] if len(image_list) > 5 else ""


        nutritional_information_fetch = sel.xpath(NUTRITIONAL_INFORMATION_XPATH)
        table = nutritional_information_fetch.xpath('.//table[@class="nutrition-table"]') if nutritional_information_fetch else ""

        def extract_nutrition_data(table_selector):
            # 1. Get Headers (Clean up whitespace and ignore the first empty <th>)
            headers = [h.strip() for h in table_selector.xpath('.//thead//th/text()').getall() if h.strip()]
            
            nutrition_dict = {}

            # 2. Iterate through rows in the tbody
            for row in table_selector.xpath('.//tbody/tr'):
                # Extract the label (e.g., "Energie", "Fats")
                key = row.xpath('normalize-space(.//td[@class="nutrition-key"]/text())').get()
                
                # Extract all values in that row (e.g., ["80 kJ", "201 kJ", "2%"])
                values = [v.strip() for v in row.xpath('.//td[@class="nutrition-value"]/text()').getall()]

                if not key or not values:
                    continue

                # Clean the key (remove trailing colons or leading dashes)
                clean_key = key.rstrip(':').lstrip('-').strip()

                # 3. Map values to headers
                # If there's only 1 header but 1 value, it maps: {"Energie": {"Per 100ml": "1.4kJ"}}
                row_map = {}
                for i, val in enumerate(values):
                    header_label = headers[i] if i < len(headers) else f"Column_{i+1}"
                    row_map[header_label] = val
                
                nutrition_dict[clean_key] = row_map

            return nutrition_dict

        nutritional_informations = extract_nutrition_data(table) if table else {}


        special_info_fetch = sel.xpath(SPECIAL_INFORMATION_XPATH).extract()
        special_infomation = "".join(special_info_fetch).replace("\n","").replace("Lifestyle","").strip() if special_info_fetch else ""

        preservation_fetch = sel.xpath(FOOD_PRESERVATION_XPATH).extract()
        food_preservation = "".join(preservation_fetch).replace("\n","").replace("Bewaring","").strip() if preservation_fetch else ""

        manufacturer_address_fetch = sel.xpath(MANUFACTURER_ADDRESS_XPATH).extract()
        manufacturer_address = "".join(manufacturer_address_fetch).replace("\n","").replace("Leveranciersadres","").strip() if manufacturer_address_fetch else ""

        site_shown_uom = product_name

        ingredients_fetch = sel.xpath(INGREDIENTS_XPATH).extract()
        ingredients_name_fetch= sel.xpath('//div[contains(@class,"attribute-ingrediënten")]//b//text()').extract_first() if ingredients_fetch else ""
        ingredients_name = ingredients_name_fetch if ingredients_name_fetch else product_name
        ingredients_text = ",".join(ingredients_fetch).replace("\n","").replace("Ingrediënten","").replace(ingredients_name,"").strip() if ingredients_fetch else ""
        ingredients = re.sub(r"\s+", " ", ingredients_text).strip().strip(",") if ingredients_text else ""


        instock_fetch = sel.xpath(INSTOCK_XPATH).extract_first()
        parsed = json.loads(instock_fetch)
        stock_status = parsed["ecommerce"]["items"][0]["stock_status"]
        instock = ""
        if stock_status == "unavailable":
            instock = False
        else:
            instock = True


        product_unique_key = f"{unique_id}P"

        item = {}
        item["unique_id"] = unique_id 
        item["competitor_name"] = competitor_name 
        item["extraction_date"] = extraction_date 
        item["product_name"] = product_name 
        item["brand"] = brand 
        item["grammage_quantity"] = grammage_quantity 
        item["grammage_unit"] = grammage_unit 
        item["producthierarchy_level1"] = producthierarchy_level1 
        item["producthierarchy_level2"] = producthierarchy_level2
        item["producthierarchy_level3"] = producthierarchy_level3 
        item["producthierarchy_level4"] = producthierarchy_level4 
        item["producthierarchy_level5"] = producthierarchy_level5 
        item["producthierarchy_level6"] = producthierarchy_level6
        item["regular_price"] = regular_price 
        item["selling_price"] = selling_price 
        item["promotion_description"] = promotion_description 
        item["price_per_unit"] = price_per_unit
        item["currency"] = currency 
        item["breadcrumb"] = breadcrumb 
        item["pdp_url"] = pdp_url 
        item["product_description"] = product_description 
        item["storage_instructions"] = storage_instructions 
        item["instructionforuse"] = instructionforuse 
        item["allergens"] = allergens 
        item["country_of_origin"] = country_of_origin 
        item["image_url_1"] = image_url_1 
        item["image_url_2"] = image_url_2
        item["image_url_3"] = image_url_3 
        item["image_url_4"] = image_url_4 
        item["image_url_5"] = image_url_5 
        item["image_url_6"] = image_url_6 
        item["nutritional_informations"] = nutritional_informations 
        item["special_infomation"] = special_infomation 
        item["food_preservation"] = food_preservation 
        item["manufacturer_address"] = manufacturer_address 
        item["site_shown_uom"] = site_shown_uom 
        item["ingredients"] = ingredients 
        item["instock"] = instock 
        item["product_unique_key"] = product_unique_key 
        logging.info(item)

        try: 
            product_item =  ProductItems(**item)
            product_item.validate()
            self.mongo_col.insert_one(item)
            logging.info("------DATA SAVED SUCCESSFULLY-----")
        except Exception as e:
            logging.info("---SAVE ERROR DUE TO %s",e)


    def close(self):
        self.mongo.close()
parser = Parser()
parser.start()
parser.close()
