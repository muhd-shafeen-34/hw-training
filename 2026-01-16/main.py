import requests as rq
import parsel as pl
from pymongo import MongoClient
import re
import json
import csv
from lxml import etree
from settings import URL, sitemapurl, header, NAMESPACE


class ParsingError(Exception):

    pass

class PlpCrawler():
    def __init__(self,url):
        self.url = url
        self.sitemapurl = sitemapurl
        self.cleaned_plp_data= []
        self.cleaned_pdp_data= []
        self.sitemap_data= []
    def start(self):
        print(f"[INFO] Starting the crawler on {self.url}")
        session = rq.Session()
        current_url = self.url
        page_no = 1
        self.unique_id = 0
        while current_url:
            try:
                print(f"Crawling Page {page_no} : {current_url}")
                response = session.get(url=current_url,headers=header)
                response.raise_for_status()

                print(response.status_code)
                self.html = response.text

                selector = pl.Selector(text=self.html)

                    #Extracting PDP links  from the url

                pdp_links = selector.xpath('//article[@data-testid="product-card"]//a[@class="product-card_c-product-card__link___7IQk"]/@href').getall()

                print(f"[INFO] Found {len(pdp_links)} product links")
                for link in pdp_links:
                    self.unique_id = self.unique_id + 1
                    full_pdp_url = f"https://www.johnlewis.com{link}"
                    details = self.parser(full_pdp_url)
                    self.cleaned_pdp_data.append(details)

                #Finding next page


                next_page = selector.xpath('//a[@class="Pagination_c-pagination__btn__QTcCg Pagination_c-pagination__next-btn__r2YUo"]/@href').get()


                if next_page:
                    current_url = f"https://www.johnlewis.com{next_page}&chunk=8"
                    page_no = page_no + 1
                else:
                    print("[INFO] No more pages found, Stopping the crawler")
                    break
            except Exception as e:
                print(f"[ERROR] Request failed: {e}")

        self.sitemap(self.sitemapurl)


        self.save_to_json()
        self.save_to_csv()



        self.mongo_connection()


    
    def parser(self,pdp_url):

        response = rq.get(url=pdp_url,headers=header)
        html = response.text
        selector = pl.Selector(text=html)
        Pdp_url = pdp_url
        image_url_fetched = selector.xpath('//img[@class="ImageMagnifier_small-image__ZK9_G"]/@src').get()
        if image_url_fetched:
            Image_url = "https:"+image_url_fetched
        else:
            Image_url = ""
        
        Brand_name = selector.xpath('//a[@id="pdp-brand-link"]/span/text()').get()
        product_name = selector.xpath('//span[@data-testid="product:title:content"]/text()').get()
        Selling_price = selector.xpath('//span[@data-testid="price-now"]/text()').get()
        Regular_price_selector = selector.xpath('//span[@data-testid="price-prev"]/text()').get()
        if Regular_price_selector:
            Regular_price = Regular_price_selector
        else:
            Regular_price = Selling_price

        Product_Description_fetched = selector.xpath('//div[contains(@class,"ProductDescriptionAccordion_descriptionContent__yd_yu")]//text()').get()
        
        if Product_Description_fetched:
            Product_Description = Product_Description_fetched
        else:
            Product_Description = ""

        Breadcrumb_fetched = selector.xpath('//ol[contains(@class,"breadcrumbs-carousel--list")]//li//text()').getall()
        clean_Breadcrumb = []
        for i in Breadcrumb_fetched:
            text = re.sub(r'\s+', ' ', i).strip()
            if text:
                clean_Breadcrumb.append(text)
        Breadcrumb = "/".join(clean_Breadcrumb)

        Category = selector.xpath('//ol[contains(@class,"breadcrumbs-carousel--list")]/li[2]//a/text()').get()

        sizes = selector.xpath('//a[@data-testid="size:option:button" and not(contains(@class,"size__label--unavailable"))]/text()').getall()
        
        Composition_fetched = selector.xpath('//dd[span[normalize-space()="Composition"]]/following-sibling::dt/text()').get()

        Composition = ""
        if Composition_fetched:
            Composition = Composition_fetched


        Care_instruction_fetched = selector.xpath('//dd[span[normalize-space()="Care instructions"]]/following-sibling::dt/text()').get()
        if Care_instruction_fetched:
            Care_instruction = Care_instruction_fetched
        else:
            Care_instruction = ""


        promotional_description_fetched =selector.xpath('//div[@data-testid="product:promotional-messages"]//text()').getall()
        if promotional_description_fetched:
            promotional = []
            for i in promotional_description_fetched:
                if i in promotional or i == "null":
                    promotional_description_fetched.remove(i)
                else:
                    promotional.append(i)
                promotional_description = ",".join(promotional)
        else:
            promotional_description = ""


        rating_fetched = selector.xpath('//span[@class="visually-hidden_visuallyHidden__sBMOc"]//text()[3]').get()
        Rating = ""
        if rating_fetched:
            Rating = re.search(r'(\d+\.\d+)',rating_fetched)
            Rating = Rating.group()

        return {
                "Unique_id" : self.unique_id,
                "Product_Name" : product_name,
                "Brand_Name" : Brand_name,
                "Category" : Category,
                "Regular_Price" : Regular_price,
                "Selling_Price" : Selling_price,
                "promotional_description" : promotional_description,
                "Breadcrumb" : Breadcrumb,
                "Pdp_url" : Pdp_url,
                "Product_Description" : Product_Description,
                "Size" : sizes,
                "Rating" : Rating,
                "Composition" : Composition,
                "Care_instruction" : Care_instruction,
                "Image_url" : Image_url
                }

    #save to json file 
    def save_to_json(self):
        if not self.cleaned_pdp_data:
            print("no data to be saved")
            return
        print("All the products are saving as a json file")
        with open("data.json","w") as file:
                    for item in self.cleaned_pdp_data:
                        json_line = json.dumps(item,ensure_ascii=False)
                        file.write(json_line + "\n")
        print(f"Completed and saved {len(self.cleaned_pdp_data)} data into json")
    
    #save to csv file

    def save_to_csv(self):
        if not self.cleaned_pdp_data:
            print("No data found to save")
            return
        print("Saving products into CSV")

        headers = self.cleaned_pdp_data[0].keys()

        with open("data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.cleaned_pdp_data)

        print(f"Saved {len(self.cleaned_pdp_data)} records successfully")

    




    #function to initiate mongo db
    
    def mongo_connection(self):
        try:
            connecion = "mongodb://localhost:27017"
            client = MongoClient(connecion)
            print(client.list_database_names())
            db = client.get_database("training_db")
            collection = db.get_collection("johnlewis")
            collection.insert_many(self.cleaned_pdp_data)
        except Exception as e:
            print(f"mongo error: {e}")
        print("suscessfully entered data into mongodb")


           #Scraping sitemap data

    def sitemap(self,url):
        print("starting to get site map index................\n")
        response = rq.get(url,headers=header)
        content = response.content
        root = etree.fromstring(content)
        if root.tag.endswith("sitemapindex"):
            print("sitemap index detected")
        self.sitemap_data = root.xpath("//ns:loc/text()",namespaces = NAMESPACE)
        print("Printing sitemap indecies..................\n")
        print(self.sitemap_data)




        
crawler = PlpCrawler(URL)
crawler.start()