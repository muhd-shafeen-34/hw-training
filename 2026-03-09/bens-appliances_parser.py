import requests
from parsel import Selector
import logging
import json
import re
import items
from settings import HEADER,CLIENT,MONGO_COLLECTION_URLS,MONGO_COLLECTION_DATA,fetch_from_mongo

class Parser():
    def __init__(self):
        self.mongo = CLIENT
        self.mongo_col = MONGO_COLLECTION_DATA

    def start(self):
        metas = fetch_from_mongo(MONGO_COLLECTION_URLS,0,"pdp_url","pdp_name","pdp_price","pdp_manufacturer")
        for meta in metas:
            pdp_url = meta["pdp_url"]
            pdp_name =  meta["pdp_name"]
            pdp_price =  meta["pdp_price"]
            pdp_manufacturer =  meta["pdp_manufacturer"]
            #pdp_url = "https://bens-appliances.com/products/samsung-icemaker-leak-moisture-kit?variant=42938992197848"
            response = requests.get(pdp_url,headers=HEADER)
            if response.status_code == 200:
                logging.warning("%s website returned status %d",pdp_url,response.status_code)
                #self.parse_item(response,pdp_name,pdp_price,pdp_manufacturer)
                self.parse_item(response)
            else:
                logging.warning(" %s website returned status code %d",pdp_url,response.status_code)
            

    #def parse_item(self,response,crawler_pdpname,crawler_pdpprice,crawler_pdpmanufacturer):
    def parse_item(self,response):
        html = response.text
        sel = Selector(text=html)
        raw_json = sel.xpath('//script[@type="application/json" and @data-product-json]/text()').extract_first()
        script_data = json.loads(raw_json)
        
        
        ### X P A T H ######
        P_NAME_XPATH = '//h1[@class="product-meta__title heading h1"]/text()'
        P_MANUFACTURER = '//a[@class="product-meta__vendor link link--accented"]/text()'
        P_AVAILABILITY = '//div[@class="product-form__payment-container"]/button/text()'
        P_DESC_XPATH = '//div[@class="card__section "]//text()'

        # if no promotion
        P_PRICE_XPATH = '//div[@class="price-list"]/span[@class="price"]/text()'

        #if promotion
        P_PRICE_SE_XPATH = '//div[@class="price-list"]/span[@class="price price--highlight"]/text()'

        #since images are loading via backend we need to get it from script
        
        SCRIPT_TAG = '//script[@type="application/json" and @data-product-json]'





        url = response.url
        title_fetch = sel.xpath(P_NAME_XPATH).extract_first()
        title = title_fetch if title_fetch else ""

        manuacturer_fetch = sel.xpath(P_MANUFACTURER).extract_first()
        manufacturer = manuacturer_fetch if manuacturer_fetch else ""   

        price_fetch = sel.xpath(P_PRICE_XPATH).extract()
        price = ""
        if price_fetch:
        
            price_clean = "".join(price_fetch).replace("\n","").replace(",","").strip().strip("")
            price = price_clean if price_clean else ""

        else:
            price_fetch = sel.xpath(P_PRICE_SE_XPATH).extract()
            price_clean = "".join(price_fetch).replace("\n","").replace(",","").strip()
            price = price_clean if price_clean else ""

        availability_fetch = sel.xpath(P_AVAILABILITY).extract_first()
        availability = ""
        if availability_fetch:
            if availability_fetch == "Sold out":
                availability = availability_fetch
            else:
                availability = "Instock"
        else:
            availability = ""

        

        #image url getting from backend
        
        image_urls_fetch = script_data["product"]["images"]
        image_urls_list = []
        if image_urls_fetch:
            for link in image_urls_fetch:
                image_urls_list.append(f"https:{link.replace("\\","")}")
        image_urls = ", ".join(image_urls_list) if image_urls_list else ""

        

        #if its available on page in a specific heading
        input_part_number_fetch = ""#sel.xpath('//span[@class="product-form__selected-value"]//text()').extract_first()
        input_part_number = ""
        if input_part_number_fetch:
            input_part_number = input_part_number_fetch
        #if not available in page we take from title
        else:
            #pattern = r'\b[A-Z]{1,4}\d{2,4}-\d{4,6}[A-Z]?\b|\b[A-Z]{1,4}\d{4,10}\b|\b\d{6,12}\b'
          # previous- pattern = r'\b[A-Z0-9]{2,}-[A-Z0-9]+\b|\b[A-Z]{1,4}\d{1,6}[A-Z]?\b|\b\d{6,12}\b'
            pattern = r'\b[A-Z0-9]{2,}-[A-Z0-9]+\b|\b[A-Z]{1,4}\d{1,6}[A-Z]?\b|\b\d{5,12}\b'
            match = re.search(pattern,title)
            input_part_number = match.group() if match else ""

        
        # if not input_part_number:
        #     pattern = r'([A-Z]{1,3}-\d{5,})$'

        #     match = re.search(pattern, url, re.I)

        #     input_part_number = match.group(1).upper() if match else ""

        if not input_part_number:
            script = sel.xpath('//script[@type="application/ld+json"][1]/text()').extract_first()
            data = json.loads(script)
            input_part_number = data.get("sku","")
            



        

        equivalent_part_no = []
        compatible_products = []
        description_fetch = sel.xpath(P_DESC_XPATH).extract()
        description = re.sub(r'\s+', ' ', " ".join(description_fetch)).strip()

        # -----------------------
        # regex patterns
        # -----------------------

        # appliance part numbers
        part_pattern = r'\b(?:[A-Z]{1,4}\d{5,}|\d{7,}|[A-Z]{2}\d{2}-\d{5}[A-Z]?)\b'

        # appliance model numbers
        model_pattern = r'\b[A-Z0-9]*\d+[A-Z]+\d+[A-Z0-9]*\b'


        # -----------------------
        # extract equivalent parts
        # -----------------------

        replace_block = re.search(
            r'(?:replace|replaces|fits|equivalent|replacement)[^:]*:\s*(.*?)(?:compatible|works|models|machine|$)',
            description,
            re.I
        )

        if replace_block:
            equivalent_part_no = re.findall(part_pattern, replace_block.group(1))


        # fallback: search whole description
        if not equivalent_part_no:
            equivalent_part_no = re.findall(part_pattern, description)


        # -----------------------
        # extract compatible models
        # -----------------------

        compatible_block = re.search(
            r'(?:compatible|works for|works with|fits models|machines)[^:]*:\s*(.*)',
            description,
            re.I
        )

        if compatible_block:
            compatible_products = re.findall(model_pattern, compatible_block.group(1))


        # fallback: search whole description
        if not compatible_products:
            compatible_products = re.findall(model_pattern, description)


        # -----------------------
        # remove part numbers from model list
        # -----------------------

        compatible_products = [
            m for m in compatible_products
            if m not in equivalent_part_no
        ]


        # -----------------------
        # remove duplicates
        # -----------------------

        equivalent_part_no = list(set(equivalent_part_no))
        compatible_products = list(set(compatible_products))
        

        # part_pattern = r'\b[A-Z]{2,}\d{2,}-\d{3,}[A-Z]?\b'

        # equivalent_part_no = []
        # compatible_products = []

    
        # # extract equivalent parts
    
        # replace_block = re.search(
        #     r'(replace|replaces|fits|equivalent|replacement)[^:]*:\s*(.*?)(compatible|works|models|machine|$)',
        #     description,
        #     re.I
        # )

        # if replace_block:
        #     equivalent_part_no = re.findall(part_pattern, replace_block.group(2))


        
        # # extract compatible models
        
        # compatible_block = re.search(
        #     r'(compatible|works for|works with|fits models|machines)[^:]*:\s*(.*)',
        #     description,
        #     re.I
        # )

        # if compatible_block:
        #     compatible_products = re.findall(part_pattern, compatible_block.group(2))


        # equivalent_part_no = list(set(equivalent_part_no))
        # compatible_products = list(set(compatible_products))

        item = {}
        item["input_part_no"] = input_part_number
        item["url"] = url
        item["title"] = title
        item["manufacturer"] = manufacturer
        item["price"] = price
        item["description"] = description
        item["availability"] = availability
        item["image_urls"] = image_urls
        item["compatible_product"] = compatible_products
        item["equivalent_par_numbers"] = equivalent_part_no
        logging.warning(item)

        try:
            product_item = items.ProductData(**item)
            product_item.validate()
            self.mongo_col.insert_one(item)
            logging.warning("-------------DATA---SAVED----SUCCESSFULLY---------------------")
        except Exception as e:
            logging.warning("--SAVE -- ERROR --- ")




        

    def close(self):
        pass

parser = Parser()
parser.start()
