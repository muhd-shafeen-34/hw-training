from pymongo import MongoClient

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

CATEGORY_API_URL = "https://www.bigbasket.com/ui-svc/v1/category-tree"
CRAWLER_API_URL = "https://www.bigbasket.com/listing-svc/v2/products"
DOMAIN = "https://www.bigbasket.com"
MONGO_URI = "mongodb://mongotraining:a4892e52373844dc4862e6c468d11b6df7938e16@209.97.183.63:27017/?authSource=admin"
CLIENT = MongoClient(MONGO_URI)
DB_NAME = "bigbasket_db"
MONGO_COLLECTION_CATEGORY = CLIENT[DB_NAME]["bigbasket_category_urls"]
MONGO_COLLECTION_URLS = CLIENT[DB_NAME]["bigbasket_urls"]
MONGO_COLLECTION_DATA = CLIENT[DB_NAME]["bigbasket_data"]


def fetch_from_mongo(collection_name,*others):
    collection = collection_name
    projection = {"_id":0}
    for field in others:
        projection[field] = 1
    results = []
    for doc in collection.find({},projection):
        if others:
            item = {}
            for field in others:
                item[field] = doc.get(field,"error")
            results.append(item)
        else:
            results.append(doc["url"])
    return results




list_of_agents = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9"]