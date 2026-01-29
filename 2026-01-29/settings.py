import requests as rq
import parsel as pq
import re
from urllib.parse import urljoin
import logging
from pymongo import MongoClient
from pathlib import Path


HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection":"keep-alive",
}
DOMAIN = "https://www.matalanme.com/ae_en"

LOG_DIR = Path("logs")

LOG_DIR.mkdir(exist_ok = True)
LOG_FILE = LOG_DIR / "matalanme.log"

logging.basicConfig(
        level = logging.INFO,
        format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(),
        ]
)
logger = logging.getLogger("matalame.log")



def save_to_mongo(data,collection):     
    try:
        connecion = "mongodb://localhost:27017"
        client = MongoClient(connecion)
        db = client.get_database("matalanme")
        collection = db.get_collection(collection)
        collection.insert_many(data)
    except Exception as e:
        logger.error(f"Mongo db eror detected\n {e}")
    print(f"suscessfully entered {len(data)} data into mongodb")

# def category_crawl(url):
#     session = rq.Session()
#     response = session.get(url=url,headers=HEADER)
#     print(response.status_code)
#     html = response.text
    
#     category_links_fetched  = re.findall(r'\\"category_link\\",\\"classes\\":null,\\"content_type\\":\\"parentcat\\",\\"link\\":\\"(.*?)\\"',html)
#     women_categories = set()
#     for i in category_links_fetched:
#         if  "women/" in i:
#             women_categories.add(urljoin(START_URL,i))
#     print(women_categories)


# category_crawl(START_URL)
