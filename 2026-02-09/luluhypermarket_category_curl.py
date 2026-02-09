from curl_cffi import requests
import parsel
from pymongo import MongoClient
import settings


class CategoryCrawler:
    def __init__(self):
        self.url = settings.URL

        self.client = MongoClient(settings.mongo_uri)
        self.collection = self.client[
            settings.db_name
        ]["category_curl"]

        # ensure url uniqueness
        self.collection.create_index("url", unique=True)

    def start(self):
        response = requests.get(
            self.url,
            headers=settings.headers,
            timeout=60,
            impersonate="chrome"  # very important
        )

        if response.status_code != 200:
            raise Exception(f"Page not available: {response.status_code}")

        selector = parsel.Selector(text=response.text)

        # exact class match (as requested)
        divs = selector.xpath('//div[@class="relative flex"]')

        print("Total categories found:", len(divs))

        inserted = 0

        for div in divs:
            href = div.xpath('.//@href').extract_first()
            name = div.xpath('.//text()').extract_first()

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
