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



                            
                            
                    
            

    