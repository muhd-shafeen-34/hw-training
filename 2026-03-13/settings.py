from pymongo import MongoClient





PDP_HEADER = {
"Host": "www.delhaize.be",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://www.delhaize.be/nl/shop/Koude-en-warme-dranken/Frisdrank/c/v2DRISOF?q=%3Arelevance&sort=relevance",
"Connection":"keep-alive",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User":"?1",
"Priority": "u=0, i",
"TE": "trailers",
}

API_HEADER = {
"Host": "www.delhaize.be",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "*/*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://www.delhaize.be/nl/shop/Waters-Softdrinks-and-Fruitsap/Frisdrank/c/v2DRISOF",
"content-type": "application/json",
"apollographql-client-name": "be-dll-web-stores",
"apollographql-client-version": "e23db29dffd65300a7defc27c5ee37a4a7c75c87",
"x-apollo-operation-name": "GetCategoryProductSearch",
"x-apollo-operation-id": "841bc048e809cf7f460d0473995516d39464c46b70952bd8b26235f881f571b5",
"x-default-gql-refresh-token-disabled": "true",
"x-dtpc":"8$133198756_784h14vWKFTRODCCQWUFFHBUVARKMEDOPPOAPJC-0e0",
"tracestate":"4888dfe3-c11c5b27@dtr=1;0b01067f40b3afee;1;b0bf94df3db180f6;1773130992774SBB0ESIOD9ELEFH2O9UBONF8ISGIGCLD;EKGUUCMFPGMDKDRWWVBUKJAMNCRUHWME-0",
"traceparent":"00-4a19e37aeb1ccfbd1aad38c25604cdc4-0b01067f40b3afee-01",
"Connection": "keep-alive",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=4",
"TE":"trailers",

}

### M O N G O DETAILS

MONGO_URI = "mongodb://mongotraining:a4892e52373844dc4862e6c468d11b6df7938e16@209.97.183.63:27017/?authSource=admin"

CLIENT = MongoClient(MONGO_URI)
DB_NAME = "delhaize_bl_db"
MONGO_COLLECTION_URLS = CLIENT[DB_NAME]["delhaize_be_urls"]
MONGO_COLLECTION_DATA = CLIENT[DB_NAME]["delhaize_be_data"]


params = {
    "operationName": "GetCategoryProductSearch",
    "variables": '{"lang":"nl","searchQuery":"","category":"v2DRISOF","pageNumber":0,"pageSize":20,"filterFlag":true,"fields":"PRODUCT_TILE","plainChildCategories":true}',
    "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"6207aa07553962b9956d475b63737d2b03b3eb7b7e6fa6ffbfc709f9894c5bdd"}}'
}

API = "https://www.delhaize.be/api/v1/"
DOMAIN = "https://www.delhaize.be"

def fetch_from_mongo(collection,limit=0,*others):
    projection = {"_id":0}
    if others:
        for field in others:
            projection[field] = 1
    result = []
    for doc in collection.find({},projection).limit(limit):
        result.append(doc)
    return result




FILE_NAME = "delhaize_be_2026_03_13_sample.csv"

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
  "handmade",
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
  "warning",
  "suitable_for",
  "standard_drinks",
  "environmental",
  "grape_variety",
  "retail_limit"
]