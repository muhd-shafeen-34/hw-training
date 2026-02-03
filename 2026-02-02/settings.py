from pymongo import MongoClient, UpdateOne, ASCENDING

"""
Settings and configuration for the Fastenal Crawler.
"""

API_URL = "https://www.fastenal.com/catalog/api/product-search"
DOMAIN = "https://www.fastenal.com"

ROOT_CATEGORY = "Electrical"
ROOT_CATEGORY_ID = "601280"

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://www.fastenal.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "X-XSRF-TOKEN": "4ed0418f-50f4-4471-bf04-fb2435da6def",
    "Cookie": (
        "XSRF-TOKEN=4ed0418f-50f4-4471-bf04-fb2435da6def; "
        "CJSESSIONID=ZjMwYWM2ZGItODdmNC00OWYzLWI2ZTYtYTZkM2Q2Y2M5Yzkw; "
        "usr_typ=external; srch_ver=v5;"
    )
}


def save_to_mongo(data_list,collection_name):
    """
    Saves a list of dictionaries to MongoDB ensuring URL uniqueness.
    """
    if not data_list:
        print("No data to save")
        return
    connecion = "mongodb://localhost:27017"
    client = MongoClient(connecion)
    db = client.get_database("Fastnel")
    collection = db.get_collection(collection_name)
    collection.create_index("url",unique=True)
    operations = [] 
    for item in data_list:
        operations.append(
            UpdateOne(
                { "url" : item["url"] },
                {"$set":item},
                upsert=True
                 
            )
        )
    try:
        result = collection.bulk_write(operations)
        print(f"Mongo Sync Complete: {result.upserted_count} new, {result.modified_count} updated.")
    except Exception as e:
        print(f"An error occurred during MongoDB sync: {e}")
    finally:
        client.close()


def fetch_from_mongo(collection_name):
    """
    Fetch latest document from MongoDB collection.
    """

    connection = "mongodb://localhost:27017"
    client = MongoClient(connection)

    db = client["Fastnel"]
    collection = db[collection_name]

    result = collection.find_one(
        {},
        {"_id": 0},
        sort=[("_id", ASCENDING)]
    )

    client.close()

    return result

def fetch_pdp_from_mongo(collection_name,limit = None):
     
   try:
        
        connecion = "mongodb://localhost:27017"
        client = MongoClient(connecion)
        db = client.get_database("Fastnel")
        collection = db.get_collection(collection_name)
        data = collection.find({},{"_id":0,})
        if limit is not None:
            data = data.limit(int(limit))
        return data
   except Exception as e:
        print("Monogoerror")









# import requests as rq
# import parsel as pq
# from urllib.parse import quote,urljoin 

# API = "https://www.fastenal.com/catalog/api/product-search"
# DOMAIN = "https://www.fastenal.com"

# root_category = "Electrical"
# root_categoryID = "601280"
# sub_category_links = []
# listing_page_links = []


# HEADER = {

# 			 "Accept": "application/json, text/plain, */*",
# 			"Accept-Encoding":"gzip, deflate, br, zstd",
			
# 				"Accept-Language": "en-US,en;q=0.9",
		
# 				 "Connection": "keep-alive",
			
# 				"Content-Length": "109",
			
# 				"Content-Type": "application/json",
			
# 				"Cookie": "XSRF-TOKEN=4ed0418f-50f4-4471-bf04-fb2435da6def; CJSESSIONID=ZjMwYWM2ZGItODdmNC00OWYzLWI2ZTYtYTZkM2Q2Y2M5Yzkw; usr_typ=external; srch_ver=v5; _ga_X40YWNGS17=GS2.1.s1770024231$o3$g0$t1770024795$j60$l0$h0; _ga=GA1.1.1889252489.1770003765",
			
# 				"Host": "www.fastenal.com",
		
# 				 "Origin": "https://www.fastenal.com",
			
# 				"Pragma": "no-cache",
		
# 				"Referer": "https://www.fastenal.com/product/Electrical?categoryId=601280",
			
# 				 "Sec-Fetch-Dest": "empty",
			
# 				 "Sec-Fetch-Mode": "cors",
			
			
# 				"Sec-Fetch-Site": "same-origin",
			
	
# 				"Sec-GPC": "1",
# 	            "TE": "trailers",
#                 "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",		
# 				 "X-XSRF-TOKEN": "4ed0418f-50f4-4471-bf04-fb2435da6def"

# }


# payload_l1 = {
#     "categoryLevelOne": root_category,
# 	"categoryId": root_categoryID,
#     "attributeFilters": {},
# 	"pageUrl":f"/product/Electrical"

# }

# session = rq.Session()
# response = session.post(API,headers=HEADER,json=payload_l1)
# print(response.status_code)
# print("root category")
# data = response.json()
# if isinstance(data, dict):
#     l1_cat = data.get("categoryList",[])
# else:
#     isinstance(data,list)
#     l1_cat = data

# if not l1_cat:
#     print("no data from api")

# for i in l1_cat:
#     if isinstance(i,dict):
#         if i.get("categoryLevelTwo",""):
#             payload_l2 = {
# 			"attributeFilters": {},
# 			"categoryId": i.get("categoryId",""),
# 			"categoryLevelOne": i.get("categoryLevelOne",""),
# 			"categoryLevelTwo": i.get("categoryLevelTwo",""),
# 			"pageUrl":f"/product/{quote(i.get("categoryLevelOne",""))}/{quote(i.get("categoryLevelTwo",""))}"
#         	}
#             sessionl2 = rq.Session()
#             responsel2 = sessionl2.post(API,headers=HEADER,json=payload_l2)
#             print(responsel2.status_code)
#             print("L2 level")
#             datal2 = responsel2.json()
#             if isinstance(datal2,dict):
#                 if datal2.get("categoryList",""):
#                     print("data2 got")
#                     l2_cat = datal2.get("categoryList","")
#                     print("l2 category fetch")
#                     for i in l2_cat:
#                         if i.get("categoryLevelThree",""):
#                             payload_l3 = {
# 									"attributeFilters": {},
# 										"categoryId": i.get("categoryId",""),
# 									"categoryLevelOne": i.get("categoryLevelOne",""),
# 									"categoryLevelThree": i.get("categoryLevelThree",""),
# 									"categoryLevelTwo": i.get("categoryLevelTwo",""),
# 									"pageUrl": f"/product/{quote(i.get("categoryLevelOne",""))}/{quote(i.get("categoryLevelTwo",""))}/{quote(i.get("categoryLevelThree",""))}"

# 							}
#                             sessionl3 = rq.Session()
#                             responsel3 = sessionl2.post(API,headers=HEADER,json=payload_l3)
#                             print(responsel3.status_code)
#                             print("level 3")
#                             datal3 = responsel3.json()
#                             if isinstance(datal3,dict):
#                                 if datal3.get("categoryList",""):
#                                     print("data3 get")
#                                     l3_cat = datal3.get("categoryList","")
#                                     for i in l3_cat:
#                                         if i.get("familyId",""):
#                                             payload_l4 = payload_l3.copy()
#                                             payload_l4.update({"categoryId": i.get("categoryId",""),"familyId":i.get("familyId","")})
#                                             sessionl4 = rq.Session()
#                                             responsel4 = sessionl4.post(API,headers=HEADER,json=payload_l4)
#                                             print(responsel4.status_code)
#                                             data4 = response.json()
#                                             if data4.get("categoryList",""):
#                                                 l4_cat = data4.get("categoryList","")
#                                             else:
#                                                 payload = payload_l4.copy()
#                                                 payload.update({"page":"1","pageSize":"12"})
#                                                 print("reached nth category")
#                                                 save = {
#                                         				"name" : payload["categoryLevelThree"],
#                                         				"url"  : urljoin(DOMAIN,payload["pageUrl"])+f"?productFamilyId={payload["familyId"]}&categoryId={payload["categoryId"]}",
#                                         				"payload" : payload
# 													}
#                                                 listing_page_links.append(save)
#                                         elif i.get("categoryLevelFour",""):
#                                             payload_l4 = payload_l3.copy()
#                                             pageurl = f"/product/{quote(i.get("categoryLevelOne",""))}/{quote(i.get("categoryLevelTwo",""))}/{quote(i.get("categoryLevelThree",""))}"
#                                             payload_l4.update({"categoryId": i.get("categoryId",""),"categoryLevelFour": i.get("categoryLevelFour",""),"pageUrl":pageurl})
#                                             sessionl4 = rq.Session()
#                                             responsel4 = sessionl4.post(API,headers=HEADER,json=payload_l4)
#                                             data4 = responsel4.json()
#                                             if data4.get("categoryList",""):
#                                                 l4_cat = data4.get("categoryList","")
#                                             else:
#                                                 payload = payload_l4.copy()
#                                                 payload.update({"page":"1","pageSize":"12"})
#                                                 print("reached nth category")
#                                                 save = {
#                                                     "name": payload["categoryLevelFour"],
#                                                     "url" : urljoin(DOMAIN,payload["pageUrl"])+f"?categoryId={payload["categoryId"]}",
#                                                     "payload" : payload
# 												}
#                                                 listing_page_links.append(save)
                                                
#                                 else:
#                                     payload = payload_l3.copy()
#                                     payload.update({"page":"1","pageSize":"12"})
#                                     print("reached nth category")

#                                     save = {
#                                         "name" : payload["categoryLevelThree"],
#                                         "url"  : urljoin(DOMAIN,payload["pageUrl"])+f"?categoryId={payload["categoryId"]}",
#                                         "payload" : payload
# 									}
#                                     listing_page_links.append(save)
                                    
# print(len(listing_page_links))
                            
            				
                            
                            
                    
            

    