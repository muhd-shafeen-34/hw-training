from playwright.sync_api import sync_playwright
from pymongo import MongoClient
from urllib.parse import urljoin
import settings


class CategoryCrawler:
    def __init__(self):
        self.start_url = settings.URL
        self.client = MongoClient(settings.mongo_uri)
        self.collection = self.client[settings.db_name]["category_playwright"]

        # ensure URL uniqueness
        self.collection.create_index("url", unique=True)

    def crawl(self):
        inserted_count = 0

        with sync_playwright() as playwright:
            browser = playwright.firefox.launch(headless=False)
            page = browser.new_page()

            page.goto(self.start_url, timeout=90_000)

            category_divs = page.locator(
                'div[class="relative flex"]'
            )

            print("Total categories found:", category_divs.count())

            for i in range(category_divs.count()):
                div = category_divs.nth(i)

                link = div.locator("a")
                name = link.locator("span").inner_text().strip()
                href = link.get_attribute("href")

                if not href or not name:
                    continue

                item = {
                    "url": urljoin(self.start_url,href.strip()),
                    "name": name,
                }

                try:
                    result = self.collection.update_one(
                        {"url": item["url"]},
                        {"$set": item},
                        upsert=True
                    )

                    if result.upserted_id:
                        inserted_count += 1

                except Exception as exc:
                    print("Mongo error:", exc)

            print(f"New categories inserted: {inserted_count}")
            input("Press ENTER to close browser...")
            browser.close()


if __name__ == "__main__":
    crawler = CategoryCrawler()
    crawler.crawl()
