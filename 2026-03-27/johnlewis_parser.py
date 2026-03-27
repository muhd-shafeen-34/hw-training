import requests
import json
from parsel import Selector
from settings import HEADER,DOMAIN,MONGO_COLLECTION_URLS,MONGO_COLLECTION_DATA,fetch_from_mongo
from urllib.parse import urljoin
from items import ProductItems
from datetime import date
import re
def parse_item(response,meta):
    sel = Selector(response.text)
#XPATH
    BRAND_XPATH = '//span[@data-testid="product:title:otherBrand"]//text()'
    BREADCRUMB_XPATH = '//ol[@class="breadcrumbs-carousel--list"]//text()'
    PROMOTION_DESCRIPTION_XPATH = '//div[@data-testid="description:content"]//text()'
    SCRIPT_DATA_XPATH = '//script[@id="__NEXT_DATA__"]/text()'


    data = sel.xpath(SCRIPT_DATA_XPATH).extract_first()
    json_data = json.loads(data)
    brand_fetch= sel.xpath(BRAND_XPATH).extract_first()
    brand = brand_fetch if brand_fetch else ""
    if not brand_fetch:
        brand = meta.get("brand","")
    

    product_description_fetch = sel.xpath(PROMOTION_DESCRIPTION_XPATH).extract_first()
    product_description = product_description_fetch if product_description_fetch else ""

    extraction_date = date.today().isoformat()

    breadcrumbs_fetch = sel.xpath(BREADCRUMB_XPATH).extract()
    breadcrumb_list = []
    breadcrumb_list = []

    for bread in breadcrumbs_fetch:
        if bread:
            bread = bread.replace("\n", "").strip()   # 🔥 assign back
            if bread:
                breadcrumb_list.append(bread)     

    page_info_fetch = json_data['props']['pageProps']['product']["attributes"]
    page_info = page_info_fetch if page_info_fetch else []

    variants_details = json_data['props']['pageProps']['product']["variants"]
    if variants_details:
        for variant in variants_details:
            unique_id = variant.get("displayCode","")
            product_name = variant.get("title","")
            price = variant.get("price",{})
            if price.get("reductionHistory",[]):
                selling_price = price.get("value","")
                regular_price = price["reductionHistory"][0].get("value")
            else:
                selling_price = price.get("value","")
                regular_price = price.get("value","")
            promotion = variant.get("messaging",[])
            if promotion:
                promotion_description = []
                for promo in promotion:
                    promotion_description.append(promo.get("title",""))
            else:
                promotion_description = ""

            pdp_url_fetch = variant.get("pdpURL",{})
            pdp_url = pdp_url_fetch.get("url","")
            size_fetch = pdp_url_fetch.get("query",{})
            size = size_fetch.get("size","") 
            color_fetch = variant.get("colour",{})
            color = color_fetch.get("trueColour","") if color_fetch else ""
            if  not color:
                color_fetch = meta.get("title","")
                color_regex  = re.search(r',\s*(.*)', color_fetch)
                color = color_fetch.group(1) if color_regex else ""


            rating =  meta.get("rating","")
            reviews = meta.get("reviews","")

            images_fetch = variant.get("images",[])
            main_image = images_fetch.get("primary","") if images_fetch else ""
            alternative = images_fetch.get("alternatives",[]) if images_fetch else []
            image_list = [main_image] + alternative
            attributes = meta.get("attributes",{})
            instock_fetch = variant.get("availability",{}) 
            instock = instock_fetch.get("availableToOrder","") if instock_fetch else ""









            item = {}
            item["unique_id"] = unique_id
            item["extraction_date"] = extraction_date
            item["product_name"] = product_name
            item["brand"] = brand
            item["regular_price"] = regular_price
            item["selling_price"] = selling_price
            item["promotion_description"] = promotion_description
            item["breadcrumb_list"] = breadcrumb_list
            item["pdp_url"] = urljoin(DOMAIN,pdp_url)
            item["product_description"] = product_description
            item["color"] = color
            item["size"] = size
            item["rating"] = rating
            item["review"] = reviews
            item["images"]= image_list
            item["attributes"] = attributes
            item["instock"] = instock
            item["pageinfo"] = page_info
            print(item)
            try:
                product_item = ProductItems(**item)
                product_item.validate()
                MONGO_COLLECTION_DATA.insert_one(item)
                print("----------data saved---------")
            except Exception as e:
                print("save error %s",e)
            

metas = fetch_from_mongo(MONGO_COLLECTION_URLS,200)
for meta in metas:
    pdp_link = meta.get("pdp_url","")

    response = requests.get(pdp_link,headers=HEADER)
    if response.status_code == 200 and response:
        parse_item(response,meta)