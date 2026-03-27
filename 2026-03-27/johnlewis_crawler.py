import requests
from settings import HEADER,DOMAIN,MONGO_COLLECTION_URLS
from urllib.parse import urljoin
from items import ProductUrls
MONGO_COLLECTION_URLS.create_index("pdp_url",unique=True)
crawler_api = "https://www.johnlewis.com/web-plp-scaffold-ui/api/product-chunk"
page = 1
params = {
    'page': page,
    'type': 'browse',
    'chunk': 1,
    'facetId': '/women/womens-nightwear/_/N-fm0',
}
def parse_item(products):
    if products:
        for prod in products:
            pdp_url = prod.get("url","")
            rating = prod.get("averageRating","")
            reviews = prod.get("reviews","")
            brand = prod.get("brand","")
            attributes = prod.get("attributes",[])
            item = {}
            item["pdp_url"] = urljoin(DOMAIN,pdp_url)
            item["rating"] = str(rating)
            item["reviews"] = str(reviews)
            item["brand"] = brand
            item["attributes"] = attributes
            print(item)
            try:
                product_item = ProductUrls(**item)
                product_item.validate()
                MONGO_COLLECTION_URLS.insert_one(item)
                print("-----DATA SAVED------")
            except Exception as e:
                print("save error due to %s",e)
        return True
    else:
        return False
            
while True:
    response = requests.get(crawler_api,headers=HEADER,params=params)

    data = response.json()
    products = data.get("products","")
    is_next = parse_item(products)
    if not is_next:
        break
    else:
        page += 1
    if page == 10:
        break
print("crawling completed")




    