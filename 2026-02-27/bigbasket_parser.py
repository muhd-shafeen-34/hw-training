
from logging import warning,error
from urllib.parse import urljoin
import items
import re
import json
import random
from datetime import date
from settings import DOMAIN,API_HEADER,CLIENT,MONGO_COLLECTION_DATA,MONGO_COLLECTION_URLS,fetch_from_mongo,html_to_text

import requests
from parsel import Selector

class Parser():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_DATA

    def start(self):

        metas = fetch_from_mongo(MONGO_COLLECTION_URLS,0,"unique_id","pdp_url","grammage_details","rating","review","images","ean_code","regular_price","selling_price")        
        for meta in metas:
            url = meta.get("pdp_url")
            _id = meta.get("unique_id")
            grammage_details = meta.get("grammage_details")
            rating = meta.get("rating")
            review = meta.get("review")
            images = meta.get("images")
            ean_code = meta.get("ean_code")
            crawler_regular_price = meta.get("regular_price")
            crawler_selling_price = meta.get("selling_price")

            response = requests.get(url,headers=API_HEADER)

            if response.status_code == 200:
                self.parse_item(response,url,_id,grammage_details,rating,review,images,ean_code,crawler_regular_price,crawler_selling_price)
            else:
                warning("%s returned response status code %d",response.url,response.status_code )

    def parse_item(self,response,url,_id,grammage_details,crawler_rating,crawler_review,images,ean,crawler_regular_price,crawler_selling_price):

        sel = Selector(response.text)
        raw_json = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first()
        script_data = json.loads(raw_json)
        data = script_data["props"]["pageProps"]["productDetails"]["children"][0]

        pdp_url = response.url
        if not pdp_url:
            pdp_url = url

        unique_id = _id
        competitor_name = "bigbasket"
        extraction_date = date.today().isoformat()

        product_name = sel.xpath('//h1[contains(@class,"sc-bMCYpw lcKFu")]/text()').extract_first()
        brand = sel.xpath('//a[contains(@class,"sc-eTYdcR iUKcjN")]/text()').extract_first()
        
        
        grammage = grammage_details.split(" ")
        if len(grammage) > 1:
            grammage_quantity = grammage[0]
            grammage_unit = grammage[1]
            site_shown_uom = grammage_details
        else:
            match = re.search(r"(\d+(?:\.\d+)?)\s*(kg|g|l|ml)\b", product_name, re.I)
            grammage = [{match.group(1)},{match.group(2)}] if match else None
            grammage_quantity = grammage[0]
            grammage_unit = grammage[1]
            site_shown_uom = " ".join(grammage)
        if grammage_unit.lower() in ["sachets","bags","tea bags","peices"]:
            grammage_unit = "pack"
            grammage_quantity = "1"
            site_shown_uom = "1 pack"
        


        bread_crumb = sel.xpath('//div[contains(@class,"Breadcrumb___StyledDiv-sc-1jdzjpl-0 dbnMCn")]//text()').extract()
        cleaned_breadcrumb = [
        item.strip()
        for item in bread_crumb
        if re.match(r'^[A-Za-z &\-]+$', item.strip())
        
        ]

        producthierarchy_level1 = cleaned_breadcrumb[0] if len(cleaned_breadcrumb) > 0 else ""
        producthierarchy_level2 = cleaned_breadcrumb[1] if len(cleaned_breadcrumb) > 1 else ""
        producthierarchy_level3 = cleaned_breadcrumb[2] if len(cleaned_breadcrumb) > 2 else ""
        producthierarchy_level4 = cleaned_breadcrumb[3] if len(cleaned_breadcrumb) > 3 else ""
        regular_price = ""
        selling_price = ""
        discount = ""
        price_was = ""
        product_description = ""
        promotion_price = ""
        
        regular_price_fetch_in_promo = sel.xpath('//td[contains(@class,"line-through p-0")]/text()').extract_first()
        if regular_price_fetch_in_promo:
            regular_price = regular_price_fetch_in_promo
            selling_price_fetch = sel.xpath('//td[contains(@class,"Description___StyledTd-sc-82a36a-0 hueIJn")]/text()').extract()
            selling_price_str = "".join(selling_price_fetch)
            m = re.search(r"₹\s*([\d]+(?:\.\d+)?)", selling_price_str)
            selling_price = m.group(1)
            price_was = regular_price_fetch_in_promo

            discount_fetch = sel.xpath('//tr[contains(@class,"flex items-center text-md text-appleGreen-700 font-semibold mb-1 leading-md p-0")]//text()').extract()
            if discount_fetch:
                promotion_description = "".join(discount_fetch)
                discount_regex = re.search(r"%\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*%", promotion_description)
                discount = next(g for g in discount_regex.groups() if g) if discount_regex else ""
                promotion_price_regex = re.search(r"(?:₹|Rs\.?)\s*(\d+(?:\.\d+)?)", promotion_description, re.I)
                promotion_price = promotion_price_regex.group(1) if promotion_price_regex else ""
            else:
                promotion_description = ""
                discount = ""
                promotion_price = ""

        else:
            regular_price_fetch = sel.xpath('//td[contains(@class,"Description___StyledTd-sc-82a36a-0 hueIJn")]/text()').extract()
            if regular_price_fetch:
                regular_price_str = "".join(regular_price_fetch)
                m = re.search(r"₹\s*([\d]+(?:\.\d+)?)", regular_price_str)
                regular_price = m.group(1)
                selling_price = regular_price
                discount = ""
                price_was = ""
                promotion_description = ""
                promotion_price = ""
            else:
                regular_price = ""
                selling_price = ""
                discount = ""
                price_was = ""
                promotion_description = ""
                promotion_price = ""
        if regular_price  == "" and selling_price == "":
                regular_price = crawler_regular_price
                selling_price = crawler_selling_price


        currency = "INR"

        bredcrumb = " > ".join(cleaned_breadcrumb)
        product_description_fetch = ""
        product_description = ""
        nutritional_info = ""
        storage_info = ""
        instructions = ""
        ingredients = ""
        ingredients = ""
        features = ""
        other_details = ""

        

        info = data["tabs"]
        for tab in info:
            if tab.get("title") == "About the Product":
                product_description_fetch = tab.get("content","") 
            elif tab.get("title") == "Nutritional Facts":
                nutritional_info = tab.get("content","")
            elif tab.get("title") == "Storage":
                storage_info = tab.get("content","")
            elif tab.get("title") == "How to Use":
                instructions = tab.get("content","")
            elif tab.get("title") == "Ingredients":
                ingredients = tab.get("content","")
            elif tab.get("title") == "Features":
                features = tab.get("content","")
            elif tab.get("title") == "Other Product Info":
                other_details = tab.get("content","")
            elif tab.get("title") == "Ingredients \u0026 Nutritional Info":
                text = tab.get("content","")
                parts = re.split(r"\bNutritional\s+Info\b", text, flags=re.I)

                ingredients = parts[0].strip()
                nutritional_info = parts[1].strip() if len(parts) > 1 else ""
            else:
                continue
        
        product_description_text = html_to_text(product_description_fetch) if product_description_fetch else ""
        cleaned_description = re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', product_description_text)).strip()
        product_description = cleaned_description if cleaned_description else ""

        nutri_info_text = html_to_text(nutritional_info)
        cleaned_nutrition = re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', nutri_info_text)).strip()
        nutritional_info = cleaned_nutrition if cleaned_nutrition else ""

        instructions_text = html_to_text(instructions) if instructions else ""
        cleaned_instructions = re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', instructions_text)).strip()
        instructions_detail = cleaned_instructions if cleaned_instructions else ""

        storage_text = html_to_text(storage_info) if storage_info else ""
        cleaned_storage =  re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', storage_text)).strip()
        storage_detail = cleaned_storage if cleaned_storage else ""

        ingredients_text = html_to_text(ingredients) if ingredients else ""
        cleaned_ingrediants = re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', ingredients_text)).strip()
        ingredients_detail = cleaned_ingrediants if cleaned_ingrediants else ""

        features_text = html_to_text(features) if features else ""
        cleaned_features = re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', features_text)).strip()
        features_detail = cleaned_features if cleaned_features else ""

        #rare case when product description contains instruction of use (prepation) details 

        preparation_regex = re.search(r"""\bprepara\w*\b\s*:?\s*(.*?)(?=\n\s*[A-Z][A-Za-z ]{2,}\n|\Z)""",product_description_text,re.I | re.S | re.X) if product_description_text else ""
        preparation_text = preparation_regex.group(1).strip() if preparation_regex  else ""
        instructions_detail = preparation_text if preparation_text else ""


        other_details_text = html_to_text(other_details)
        if other_details_text:
            country_fetch = re.search(r"Country\s*of\s*Origin\s*:\s*(.*?)(?=\s*(?:Manufactured|Marketed|Best|For\s+Queries|$))",other_details_text,re.I)
            country_of_origin = country_fetch.group(1).strip() if country_fetch else ""
            #manufacturer = re.search(r"Manufacture(?:d by|r Name & Address):\s*(.*?)(?=\s*(?:Country of Origin|Country Of Origin|Best before|For Queries|Marketed by|$))",other_details_text,re.I | re.S)
            #manufacturer = re.search(r"(?:Manufactured by|Manufactured\s*&\s*Marketed by|Manufacturer Name\s*&\s*Address)\s*:\s*(.*?)(?=\s*(?:Country of Origin|Country Of Origin|Best before|For Queries|Marketed by|$))",other_details_text,re.I | re.S)
            #manufacturer = re.search(r"""\bmanufactur\w*[^:]{0,40}:\s*(.*?)(?=\s*\b(?:EAN|FSSAI|Country|Best|Disclaimer|For\s+Queries|Marketed|$))""",other_details_text,re.I | re.S | re.X)
            manufacturer = re.search(r"""\bmanufactur\w*(?:\s+name\s*&?\s*address)?(?:\s*&\s*marketed\s+by)?(?:\s+by)?\s*:?\s*(.*?)(?=\s*\b(?:marketed\s+by|fssai|country|best\s+before|disclaimer|for\s+queries|ean|lic|import|$))""",other_details_text,re.I | re.S | re.X)
            manufacturer_details_fetch = manufacturer.group(1).strip() if manufacturer else ""
            cleaned_manufacturer = re.sub(r'\s+', ' ', re.sub(r'@import\s+url\([^)]*\);\s*', '', manufacturer_details_fetch)).strip()
            manufacturer_details = cleaned_manufacturer if cleaned_manufacturer else ""
            ean_code_fetch = re.search(r"ean\s*code\s*:\s*(\d+)", other_details_text, re.IGNORECASE)
            ean_code = ean_code_fetch.group(1) if ean_code_fetch else "" 
        else:
            country_of_origin = ""
            manufacturer_details = ""
            ean_code = ""
        
        eancode = ean
        if not eancode:
            eancode = ean_code

        rating  = crawler_rating
        review = crawler_review

        image = images  # your list of image URL   s

        image_url_1 = image[0] if len(image) > 0 else ""
        image_url_2 = image[1] if len(image) > 1 else ""
        image_url_3 = image[2] if len(image) > 2 else ""
        image_url_4 = image[3] if len(image) > 3 else ""
        image_url_5 = image[4] if len(image) > 4 else ""
        image_url_6 = image[5] if len(image) > 5 else ""

        instock = ""
        instock_fetch = sel.xpath('//button[@class="Button-sc-1dr2sn8-0 sc-jGKxIK dEdziT kCeaPI"]')

        if instock_fetch:
            instock = False
        else:
            instock = True
        product_unique_key =  f"{unique_id}P"
    
        item = {}
        item["unique_id"] = unique_id
        item["product_name"] = product_name
        item["brand"] = brand
        item["pdp_url"] = pdp_url
        item["competitor_name"] = competitor_name
        item["extraction_date"] = extraction_date
        item["grammage_quantity"] = grammage_quantity
        item["grammage_unit"] = grammage_unit
        item["regular_price"] = regular_price
        item["selling_price"] = selling_price
        item["currency"] = currency
        item["price_was"] = price_was
        item["promotion_price"] = promotion_price
        item["percentage_discount"] = discount
        item["promotion_description"] = promotion_description
        item["producthierarchy_level1"] = producthierarchy_level1
        item["producthierarchy_level2"] = producthierarchy_level2
        item["producthierarchy_level3"] = producthierarchy_level3
        item["producthierarchy_level4"] = producthierarchy_level4
        item["breadcrumb"]  = bredcrumb
        item["product_description"] = product_description
        item["storage_instructions"] = storage_detail
        item["instructionforuse"] = instructions_detail
        item["nutritional_information"] = nutritional_info
        item["country_of_origin"] = country_of_origin
        item["features"] = features_detail
        item["manufacturer_address"] = manufacturer_details
        item["ingredients"] = ingredients_detail
        item["rating"] = rating
        item["review"] = review
        item["instock"] = instock
        item["image_url_1"] = image_url_1
        item["image_url_2"] = image_url_2
        item["image_url_3"] = image_url_3
        item["image_url_4"] = image_url_4
        item["image_url_5"] = image_url_5
        item["image_url_6"] = image_url_6
        item["site_shown_uom"] = site_shown_uom
        item["competitor_product_key"] = eancode
        item["product_unique_key"] = product_unique_key
        print(item)
        try:
            product_item = items.Product(**item)
            product_item.validate()
            MONGO_COLLECTION_DATA.insert_one(item)
            warning("---SAVED SUCCESSFULLY----")

        except Exception as e:
            warning("------save errror---- due to %s",e)

    def close(self):
        self.mongo.close()






parser = Parser()
parser.start()





        





























# for link in links:
#     response = requests.get(link,headers=API_HEADER)
#     print(response.status_code)
#     sel = Selector(response.text)
#     raw_json = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first()
#     script_data = json.loads(raw_json)
#     data = script_data["props"]["pageProps"]["productDetails"]["children"][0]
#     print(data.keys())



    
    
#     product_name = sel.xpath('//h1[contains(@class,"sc-bMCYpw lcKFu")]/text()').extract_first()
#     print(product_name)
#     match = re.search(r"(\d+(?:\.\d+)?)\s*(kg|g|l|ml)\b", product_name, re.I)
#     pack_size = f"{match.group(1)} {match.group(2)}" if match else None
#     print(pack_size)
#     brand = sel.xpath('//a[contains(@class,"sc-eTYdcR iUKcjN")]/text()').extract_first()
#     print(brand)
#     regular_price_fetch_in_promo = sel.xpath('//td[contains(@class,"line-through p-0")]/text()').extract_first()
#     if regular_price_fetch_in_promo:
#         regular_price = regular_price_fetch_in_promo
#         selling_price_fetch = sel.xpath('//td[contains(@class,"Description___StyledTd-sc-82a36a-0 hueIJn")]/text()').extract()
#         selling_price = selling_price_fetch[-1]
#         discount_fetch = sel.xpath('//td[contains(@class,"text-md text-appleGreen-700 font-semibold p-0")]/text()').extract_first()
#         if discount_fetch:
#             discount_regex = re.search(r"(\d+(?:\.\d+)?)\s*%", discount_fetch)
#             discount = discount_regex.group(1) if discount_regex else ""
#         else:
#             discount = ""
#     else:
#         regular_price_fetch = sel.xpath('//td[contains(@class,"Description___StyledTd-sc-82a36a-0 hueIJn")]/text()').extract()
#         regular_price = regular_price_fetch[-1]
#         selling_price = regular_price

#     print(regular_price)
#     print(selling_price)
#     print(discount)

#     bread_crumb = sel.xpath('//div[contains(@class,"Breadcrumb___StyledDiv-sc-1jdzjpl-0 dbnMCn")]//text()').extract()
#     print(bread_crumb)
#     cleaned_breadcrumb = [
#     item.strip()
#     for item in bread_crumb
#     if re.match(r'^[A-Za-z &]+$', item.strip())
#     ]
#     print(cleaned_breadcrumb)

#     info = data["tabs"]
#     for tab in info:
#         if tab.get("title") == "About the Product":
#             product_description_fetch = tab.get("content") 
#         elif tab.get("title") == "Nutritional Facts":
#             nutritional_info = tab.get("content")
#         elif tab.get("title") == "Storage":
#             storage_info = tab.get("content")
#         elif tab.get("title") == "How to Use":
#             instructions = tab.get("content")
#         elif tab.get("title") == "Ingredients":
#             ingredients = tab.get("content")
#         elif tab.get("title") == "Features":
#             features = tab.get("content")
#         elif tab.get("title") == "Other Product Info":
#             other_details = tab.get("content")
#         else:
#             continue
        

#     if product_description_fetch:
#         print(html_to_text(product_description_fetch).strip())

#         print(html_to_text(nutritional_info))
#     if other_details:
#         details = html_to_text(other_details)
#         country_fetch = re.search(r"Country\s*Of\s*Origin\s*:\s*([A-Za-z ]+)",details,re.I)
#         country_of_origin = country_fetch.group(1).strip() if country_fetch else None 
#         manufacturer = re.search(r"Manufacture(?:d by|r Name & Address):\s*(.*?)(?=\s*Best before|For Queries|$)",details,re.I | re.S)
#         manufacturer_details = manufacturer.group(1).strip() if manufacturer else None
#     print(country_of_origin)
#     print(manufacturer_details)

    




#     raw = sel.xpath('//div[@class="sc-bJBgwP jjYhX"]/div[@class="overflow-hidden"]')
#     if raw:
#         inner = Selector(raw.text)
#         print(inner)
#     else:
#         print("not fetched")

