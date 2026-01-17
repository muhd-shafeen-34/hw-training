import requests as rq
import parsel as pl
import re
from pymongo import MongoClient

URL = "https://www.johnlewis.com/browse/men/mens-shirts/_/N-eaf?chunk=8"
header = {
    'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
    }







# def parser(pdp_url):
#     response = rq.get(url=pdp_url,headers=header)
#     html = response.text
#     print(response.status_code)
#     selector = pl.Selector(text=html)
#     Product_Description = selector.xpath().get()
#   uurl = f"https://www.johnlewis.com{image_url_fetched}"
#     return Product_Description
#         image_url = "https:"+image_url_fetched
#         sizes = selector.xpath('//ul[contains(@class,"size_c-sizeList__items__HFUww Sizes_groupList__91NBu")]//li//text()').getall()
        
#         promotional_description_fetched =selector.xpath('//div[@data-testid="product:promotional-messages"]//text()').getall()
#         if promotional_description_fetched:
#             promotional = []
#             for i in promotional_description_fetched:
#                 if i in promotional or i == "null":
#                         promotional_description_fetched.remove(i)
#                 else:
#                         promotional.append(i)
#             promotional_description = ",".join(promotional)
#         else:
#               promotional_description = ""

#         rating_fetched = selector.xpath('//span[@class="visually-hidden_visuallyHidden__sBMOc"]//text()[3]').get()
#         rating = re.search(r'(\d+\.\d+)',rating_fetched)
#         rating = rating.group()

# def mongo_connection(document):
#     try:
#         connecion = "mongodb://localhost:27017"
#         client = MongoClient(connecion)
#         print(client.list_database_names())
#         db = client.get_database("training_db")
#         collection = db.get_collection("johnlewis")
#         collection.insert_many(document)
#     except Exception as e:
#         print(f"mongo error: {e}")
#     print("suscessfully entered data into mongodb")

# mongo_connection(document={"hello":"this is data"})

        

#         # return f"details of page brand name = {Brand_name},\n product name = {product_name}"
    
#print(parser("https://www.johnlewis.com/john-lewis-regular-fit-linen-shirt/white-old/p6172177"))