import requests as rq
from pathlib import Path
import logging
from pymongo import MongoClient,UpdateOne
header = {
     
     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
     "Accept-Encoding":"gzip, deflate, br, zstd",

    "Accept-Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",

   "Host":"www.academy.com",
    "Referer":"https://www.academy.com/c/mens?&facet=%27facet_Price%27:%3E%20500",
    "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
}       
url = "https://www.academy.com/"


MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "academy_poc_2026_02_16"
CATEGORY_COLLECTION_NAME = "academy_product_category_urls"



LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "academy.log"

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),

    ]
)

logger = logging.getLogger("academy_scraper")


def save_to_mongo(data, collection_name):
    if not data:
        print("No data provided to save.")
        return

    try:
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][collection_name]
        collection.create_index("url", unique=True)

        operations = [
            UpdateOne(
                {"url": doc["url"]},
                {"$set": doc},
                upsert=True
            )
            for doc in data
            if "url" in doc
        ]

        if not operations:
            print("No valid documents to insert.")
            return

        result = collection.bulk_write(operations, ordered=False)
        print(
            f"Matched: {result.matched_count} | "
            f"Upserted: {len(result.upserted_ids)} | "
            f"Modified: {result.modified_count}"
        )

    except Exception as e:
        logger.exception("Mongo save failed")
# response = rq.get(url,headers=header)
# print(response.status_code)
# print(response.text)