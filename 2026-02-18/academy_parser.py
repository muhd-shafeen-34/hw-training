import requests as rq
import parsel as pq
import settings
import re
import academy_items
import time
from browserforge.headers import HeaderGenerator

class Parser():
    def __init__(self):
        self.logger = settings.logger

    def start(self):
        '''starting functions'''
        # here am fetching urls and rating from mongodb
        metas = settings.fetch_from_mongo(settings.PDP_URLS_COLLECTION_NAME,"rating","review")
        for meta in metas:
            url = meta.get("url")
            rating = meta.get("rating")
            review = meta.get("review")
            time.sleep(3)
            headers = HeaderGenerator()
            header = headers.generate()
            header["Host"] = "www.academy.com"
            header["Cookie"] = "" #pass cookie here optional
            session = rq.Session()
            session.headers.update(header)
            response = session.get(url)
            self.logger.info("website shows %d",response.status_code)
            if response.status_code == 200:
                self.logger.info("currently parsing %s",response.url)
                self.parse_item(url,response,rating,review)
            else:
                self.logger.info("website blocked")

    def parse_item(self,pdp_url,response,pdp_rating,pdp_review):
        html = response.text
        selector = pq.Selector(text=html)

        ##---- XPATH AND REGEX --#####

        UNIQUE_ID_XPATH = '//div[@data-auid="product-sku-and-item-data"]//span[normalize-space(text())="SKU:"]/following-sibling::span/text()'
        PRODUCT_NAME_XPATH = '//h1[@data-auid="PDP_ProductName"]/text()'
        SELLING_PRICE_XPATH = '//div[@data-auid="nowPrice"]//span[@class="pricing nowPrice lg "]/text()'

        #if selling price available
        SEL_REGULAR_PRICE_XPATH = '//div[@data-auid="nowPrice"]//span[@class="pricing wasPrice lg"]/text()'
        DISCOUNT_XPATH = '//div[@data-auid="nowPrice"]//span[@class="pricing priceSaving lg"]/text()'

        #if selling price not available
        REGULAR_PRICE_XPATH = '//div[@data-auid="regPrice"]/span[@class="pricing nowPrice lg"]/text()'

        DESCRIPTION_XPATH = '//div[contains(@class,"detailPanel--jmOfo")]//div[contains(@class,"textBodyLg")]/text()'
        SPECIFICATIONS_XPATH = '//h4[normalize-space(text())="Specifications"]/following-sibling::div//li/text()'
        IMAGE_URL_XPATH = '//div[@class="carousel--gtD0D carousel--OoEc8"]//@src'







        # brand name is not availabe via xpath so getting from page source in script tag using regex

        BRAND_NAME_REGEX = r'"@type"\s*:\s*"Brand"\s*,\s*"name"\s*:\s*"([^"]+)"'
        SIZE_REGEX = r'"facet_Size"\s*:\s*\[\s*"([^"]+)"\s*\]'
        SIZE_ELSE_REGEX = r'"name"\s*:\s*"Shoe Size"\s*,\s*"value"\s*:\s*"([^"]+)"'

            #COLOR_REGEX need cleaned unique id
            #reviews need api request
            #raring is passed from function no xpath needed

        ##---- EXTRACT AND CLEAN DATA ----####
        self.logger.info("extracting.................................")

        url = pdp_url

        unique_id_fetch = selector.xpath(UNIQUE_ID_XPATH).extract()
        unique_id = "".join(unique_id_fetch).strip()
        product_name_fetch = selector.xpath(PRODUCT_NAME_XPATH).extract_first()
        product_name = product_name_fetch.strip() if product_name_fetch else ""

        brand_name_match = re.search(BRAND_NAME_REGEX,html)
        brand_name = brand_name_match.group(1) if brand_name_match else None


        selling_price_fetch = selector.xpath(SELLING_PRICE_XPATH).extract_first()
        if selling_price_fetch:
            selling_price = selling_price_fetch.strip("$")
            regular_price_fetch = selector.xpath(SEL_REGULAR_PRICE_XPATH).extract_first()
            regular_price = regular_price_fetch.strip("$") if regular_price_fetch else ""
            discount_fetch = selector.xpath(DISCOUNT_XPATH).extract_first()
            discount_fetch_regex  = re.search(r'(\d+(?:\.\d+)?)%', discount_fetch)
            discount = discount_fetch_regex.group(1) if discount_fetch_regex else ""
        else:
            regular_price_fetch = selector.xpath(REGULAR_PRICE_XPATH).extract_first()
            regular_price = regular_price_fetch.strip("$") if regular_price_fetch else ""
            selling_price = regular_price_fetch.strip("$") if regular_price_fetch else ""
            discount = ""
        

        description_fetch = selector.xpath(DESCRIPTION_XPATH).extract_first()
        description = description_fetch.strip() if description_fetch else ""


        specifications_fetch = selector.xpath(SPECIFICATIONS_XPATH).extract()
        if specifications_fetch:
            specifications = dict(
            item.split(":", 1)
            for item in specifications_fetch
            if ":" in item
                    )
        else:
            specifications = ""



        image_url_fetch = selector.xpath(IMAGE_URL_XPATH).extract()
        
        image_url_list = [f"https:{image_url_clean.replace('-thumbnails','')}" for image_url_clean in image_url_fetch] if image_url_fetch else ""
        image_url = ",".join(image_url_list) if image_url_list else ""


        color_fetch_pattern = rf'"vendorColorName"\s*:\s*"([^"]+)".*?"itemId"\s*:\s*"{unique_id}"'
        color_fetch_match = re.search(color_fetch_pattern,html,re.DOTALL)
        color = color_fetch_match.group(1) if color_fetch_match else ""
        
        
        size_fetch = set(re.findall(SIZE_REGEX, html))
        if size_fetch:
            size_list = list(size_fetch) if size_fetch else ""
            size = ",".join(size_list) if size_list else ""
        else:
            size_fetch = set(re.findall(SIZE_ELSE_REGEX,html))
            size_list = [sizes for sizes in size_fetch if sizes != "0"] if size_fetch else ""
            size = ""

        rating_fetch = pdp_rating
        rating = rating_fetch if rating_fetch != "0.0" or "0" else ""

        review_fetch = pdp_review
        review = review_fetch if review_fetch != "0" or "0.0" else ""


        # if rating_fetch and rating_fetch != "0.0":

        # #     rating = rating_fetch

        # #     api_identifier_match = re.search(r'"parentPartNumber"\s*:\s*"([^"]+)"', html)
        # #     api_indentifier = api_identifier_match.group(1) if api_identifier_match else ""
            
        # #     if api_indentifier:

        # #         api_params = settings.get_bv_review_params(api_indentifier)

        # #         api_response = rq.get(url=settings.api_url,headers=settings.review_api_header,params=api_params)
        # #         print(api_response.status_code)
        # #         data = api_response.json()
        # #         reviews = []
        # #         api_details = data["response"]
        # #         if api_details:
        # #             review_details = api_details["Results"]
        # #             if review_details:
        # #                 for doc in review_details:
        # #                     reviews.append(doc['ReviewText'])
        # #             else:
        # #                 reviews = ""
        # #     else:
        # #         reviews = ""
        # #         rating = rating_fetch
        # # else:
        # #     reviews = ""
        # #     rating = ""


        ### ---- ITEM YIELD ---- ####

        item = {}
        item["unique_id"] = unique_id
        item["url"] = url
        item["productname"] = product_name
        item["brand"] = brand_name
        item["selling_price"] = selling_price
        item["regular_price"] = regular_price
        item["discount"] = discount
        item["description"] = description
        item["specifications"] = specifications
        item["image_url"] = image_url
        item["color"] = color
        item["size"] = size
        item["rating"] = rating
        item["review"] = review
        item["fit_type"] = ""

        self.logger.info(item)
        try:
            product_item = academy_items.ProductItem(**item)
            product_item.validate()
            settings.MONGO_COLLECTION_DATA.insert_one(item)
            # product_item = academy_items.ProductItem(**item)
            # product_item.save()
        except Exception as e:
            self.logger.info("save eroor due to %s",e)









        
        



        


parser = Parser()
parser.start()

















