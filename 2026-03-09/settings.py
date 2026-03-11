from pymongo import MongoClient



START_URL = "https://bens-appliances.com/collections/all"
DOMAIN = "https://bens-appliances.com"

HEADER = {
    "Host": "bens-appliances.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://bens-appliances.com/",
"Connection": "keep-alive",
"Cookie": "localization=IN; cart_currency=INR; _shopify_y=26995a7b-20f4-48ef-8a6e-4c9b2fc01786; _shopify_s=e9159a72-23fc-428f-a80a-8f8d4a762764; _shopify_essential=:AZy8Sb80AAEAluzIVCP0EYrktRwacGvOaqS1CtiPpkKmKPM9vh-eqRgVsjDDFB23VQfqPVBuey_4DM9Bs88kK5F72nMlO6BFQSpkoW0EYVPDwhmNkoY_50acqkc_5jWfH4cm9y9WdU1KjJE6Lax_Hea-WdCi2Esa2c9nfxIiCFpCq1FxA_5odR3UBSp2LvsFbvvT_5dOR-EON-O3thXVq0BYtGP1LDNA7Ue7v0SdR8kQUBimlPK8EeinrxsfW9N-7SYkcCM7UQCDGhx9U-vkjpJozWggJxtEGLUJIFSShGn2G7maSj-60-A18io7oeFQSHFuwPD3Jj8NJL2h074BuNV_YIAnCOjlQu1XFMiVT_WnLseg8516WShRJnZ23Ws7OXCH0_EYouPMs7qhXzDkqqTvnBej5CWX2ORTItxzvg:; _shopify_analytics=:AZy8ScDXAAEA-ZbtdoovSNIx_pIm09XOEyFtdo4aWmpZNZ0fcgIb4Dm2-ZGaCzZfk6OeQZSr6jxB_Em0JEWwZvFCeMw:; _ga_DCFNY9E0XR=GS2.1.s1772685480$o1$g1$t1772687555$j45$l0$h0; _ga=GA1.1.1193578771.1772685481; _ga_Z1RVEG15EB=GS2.1.s1772685479$o1$g1$t1772687555$j45$l0$h0; _ga_79LJR1R713=GS2.1.s1772685480$o1$g1$t1772687555$j45$l0$h0; _ga_V7N0GGJLMB=GS2.1.s1772685480$o1$g1$t1772687640$j59$l0$h0; _ga_L8K02GV0WK=GS2.1.s1772685480$o1$g1$t1772687640$j26$l0$h0; _gid=GA1.2.1127470842.1772685481; _ttp=01KJY4KQ049CA87RW6FQSJRW27_.tt.0; ttcsid_D3RQL7JC77U4FIU0R4GG=1772685483019::Afj9SVu1LzjnYZoLqJxu.1.1772687556712.0; ttcsid=1772685483020::jDZk4F2eaRKPUIiweqYz.1.1772687556716.0; _fbp=fb.1.1772685483221.951173941873322768; lo-uid=c866c4ab-1772685485626-1eb414c4fa488317; lo-visits=2",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"If-None-Match": "page_cache:57580716190:CollectionDetailsController:a8320f608bdee467b2880678ea419f61",
"Priority": "u=0,i",
}


MONGO_URI = "mongodb://mongotraining:a4892e52373844dc4862e6c468d11b6df7938e16@209.97.183.63:27017/?authSource=admin"
CLIENT = MongoClient(MONGO_URI)
DB_NAME = "bens-appliances_db"

MONGO_COLLECTION_URLS = CLIENT[DB_NAME]["bens-appliances_urls_2026_03_10"]
MONGO_COLLECTION_DATA = CLIENT[DB_NAME]["bens-appliances_data_2026_03_11"]


def fetch_from_mongo(collection,limit,*others):
    projection = {"_id":0}
    if others:
        for field in others:
            projection[field] = 1
    results = []
    for doc in collection.find({},projection).limit(limit):
        if others:
            item = {}
            for field in others:
                item[field] = doc.get(field,"")
            results.append(item)
        else:
            results.append({"pdp_url":doc.get("pdp_url","")})
            
    return results

FILE_NAME = "bens_appliances_2026_03_11_sample.csv"
FILE_HEADER = ["input_part_number", "url", "title", "manufacturer", "price", "description", "oem_part_number", "retailer_part_number", "competitor_part_numbers", "compatible_products", "equivalent_part_numbers", "product_specfications", "additional_description", "availability", "image_urls", "linked_files"]