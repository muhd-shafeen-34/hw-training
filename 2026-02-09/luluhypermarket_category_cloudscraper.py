# import cloudscraper 
# import settings 
# import parsel 
# scraper = cloudscraper.create_scraper() 
# url = settings.URL 
# response = scraper.get(url,headers=settings.headers)
# print(response.status_code)





import cloudscraper
import parsel
from pymongo import MongoClient
import settings


class CategoryCrawler:
    def __init__(self):
        self.url = settings.URL
        self.scraper = cloudscraper.create_scraper()

        self.client = MongoClient(settings.mongo_uri)
        self.collection = self.client[
            settings.db_name
        ]["category_cloudscraper"]

        # make url unique
        self.collection.create_index("url", unique=True)

    def start(self):
        response = self.scraper.get(self.url, headers=settings.headers)

        if response.status_code != 200:
            raise Exception("Page not available")
        html = response.text
        selector = parsel.Selector(text=html)
        
        # exact class match
        divs = selector.xpath('//div[@class="relative flex"]').extract()

        print("Total categories found:", len(divs))

        inserted = 0

        for div in divs:
            href = div.xpath('.//@href').get()
            name = div.xpath('.//text()').get()

            if not href or not name:
                continue

            item = {
                "url": href.strip(),
                "name": name.strip(),
            }

            result = self.collection.update_one(
                {"url": item["url"]},
                {"$set": item},
                upsert=True
            )

            if result.upserted_id:
                inserted += 1

        print("New categories inserted:", inserted)


if __name__ == "__main__":
    crawler = CategoryCrawler()
    crawler.start()
