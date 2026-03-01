from pymongo import MongoClient
from parsel import Selector

API_HEADER = {
"Host": "www.bigbasket.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
"Accept": "*/*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"X-Channel": "BB-WEB",
"Content-Type": "application/json",
"X-Tracker": "d95f4947-2b47-4fb6-9ac8-db514a869d39",
"osmos-enabled": "true",
"common-client-static-version": "101",
"X-Entry-Context": "bbnow",
"X-Entry-Context-Id": "10",
"X-Integrated-FC-Door-Visible": "false",
"Connection": "keep-alive",
"Cookie": """_bb_locSrc=default; x-channel=web; _bb_aid="MjkxMzA4NDUzMA=="; _bb_cid=1; _bb_vid=MTEzOTY1MTM0NjMyNzkyMDM2Ng==; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=GNNL0GlYQ7wO2s2zLnxemxPVG0QRdaqskejGdCk1a2gLP7N6hqqFaNDikdk84OQM; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; _bb_pin_code=; _bb_sa_ids=19224; _is_tobacco_enabled=1; _is_bb1.0_supported=0; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjE5MjI0; is_integrated_sa=1; is_subscribe_sa=0; bb2_enabled=true; jarvis-id=89a7729a-31e7-4f6b-a31b-0d3c2c5b7d3f; _gcl_au=1.1.260775474.1771995716; adb=0; ufi=1; _ga_FRRYG5VKHX=GS2.1.s1772013081$o4$g1$t1772019058$j60$l0$h0; _ga=GA1.2.2064446638.1771995717; bigbasket.com=a37f10dd-b685-4b19-94b7-7e3bd5889a00; _gid=GA1.2.1507038067.1771995718; _fbp=fb.1.1771995718589.84402057250333783; _client_version=2843; _bb_hid=7427; sessionid=mzpzcw42y06l4phxtjcto9lua3wmtlkt; _bb_tc=0; _bb_rdt="MzEwNzM5NzQwMA==.0"; _bb_rd=6; csurftoken=lQN43Q.MTEzOTY1MTM0NjMyNzkyMDM2Ng==.1772019080133.M8IL2Pkx6mwsIT4sDKNDXDOta+K5WO3KRIhpzG7BQvY=; ts=2026-02-25%2017:00:58.712; _gat_UA-27455376-1=1""",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=4",
"TE": "trailers",
}

#--------URLS------------

CATEGORY_API_URL = "https://www.bigbasket.com/ui-svc/v1/category-tree"
CRAWLER_API_URL = "https://www.bigbasket.com/listing-svc/v2/products"
DOMAIN = "https://www.bigbasket.com"

#----------MONGO-CONNECTION----------

MONGO_URI = "mongodb://mongotraining:a4892e52373844dc4862e6c468d11b6df7938e16@209.97.183.63:27017/?authSource=admin"
CLIENT = MongoClient(MONGO_URI)
DB_NAME = "bigbasket_db"
MONGO_COLLECTION_CATEGORY = CLIENT[DB_NAME]["bigbasket_category_urls"]
MONGO_COLLECTION_URLS = CLIENT[DB_NAME]["bigbasket_urls"]
MONGO_COLLECTION_DATA = CLIENT[DB_NAME]["bigbasket_data"]


def fetch_from_mongo(collection_name,limit=0,*others):
    collection = collection_name
    projection = {"_id":0}
    for field in others:
        projection[field] = 1
    results = []
    for doc in collection.find({},projection).limit(limit):
        if others:
            item = {}
            for field in others:
                item[field] = doc.get(field,"error")
            results.append(item)
        else:
            results.append(doc["url"])
    return results


def html_to_text(data):
    return " ".join(Selector(text=data).xpath("//text()").extract()).strip()


FILE_NAME = "bigbasket_2026_02_27_sample(3).csv"

FILE_HEADER= [
  "unique_id",
  "competitor_name",
  "store_name",
  "store_addressline1",
  "store_addressline2",
  "store_suburb",
  "store_state",
  "store_postcode",
  "store_addressid",
  "extraction_date",
  "product_name",
  "brand",
  "brand_type",
  "grammage_quantity",
  "grammage_unit",
  "drained_weight",
  "producthierarchy_level1",
  "producthierarchy_level2",
  "producthierarchy_level3",
  "producthierarchy_level4",
  "producthierarchy_level5",
  "producthierarchy_level6",
  "producthierarchy_level7",
  "regular_price",
  "selling_price",
  "price_was",
  "promotion_price",
  "promotion_valid_from",
  "promotion_valid_upto",
  "promotion_type",
  "percentage_discount",
  "promotion_description",
  "package_sizeof_sellingprice",
  "per_unit_sizedescription",
  "price_valid_from",
  "price_per_unit",
  "multi_buy_item_count",
  "multi_buy_items_price_total",
  "currency",
  "breadcrumb",
  "pdp_url",
  "variants",
  "product_description",
  "instructions",
  "storage_instructions",
  "preparationinstructions",
  "instructionforuse",
  "country_of_origin",
  "allergens",
  "age_of_the_product",
  "age_recommendations",
  "flavour",
  "nutritions",
  "nutritional_information",
  "vitamins",
  "labelling",
  "grade",
  "region",
  "packaging",
  "receipies",
  "processed_food",
  "barcode",
  "frozen",
  "chilled",
  "organictype",
  "cooking_part",
  "Handmade",
  "max_heating_temperature",
  "special_information",
  "label_information",
  "dimensions",
  "special_nutrition_purpose",
  "feeding_recommendation",
  "warranty",
  "color",
  "model_number",
  "material",
  "usp",
  "dosage_recommendation",
  "tasting_note",
  "food_preservation",
  "size",
  "rating",
  "review",
  "file_name_1",
  "image_url_1",
  "file_name_2",
  "image_url_2",
  "file_name_3",
  "image_url_3",
  "file_name_4",
  "image_url_4",  
  "file_name_5",
  "image_url_5",
  "file_name_6",  
  "image_url_6",
  "competitor_product_key",
  "fit_guide",
  "occasion",
  "material_composition",
  "style",
  "care_instructions",
  "heel_type",
  "heel_height",
  "upc",
  "features",
  "dietary_lifestyle",
  "manufacturer_address",
  "importer_address",
  "distributor_address",
  "vinification_details",
  "recycling_information",
  "return_address",
  "alchol_by_volume",
  "beer_deg",
  "netcontent",
  "netweight",
  "site_shown_uom",
  "ingredients",
  "random_weight_flag",
  "instock",
  "promo_limit",
  "product_unique_key",
  "multibuy_items_pricesingle",
  "perfect_match",
  "servings_per_pack",
  "Warning",
  "suitable_for",
  "standard_drinks",
  "environmental",
  "grape_variety",
  "retail_limit"
]