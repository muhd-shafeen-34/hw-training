from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import settings


class CategoryCrawler:
    def __init__(self):
        self.start_url = settings.URL
        self.client = MongoClient(settings.mongo_uri)
        self.collection = self.client[settings.db_name]["category_salenium"]

        # ensure URL uniqueness
        self.collection.create_index("url", unique=True)

    def crawl(self):
        inserted_count = 0

        options = Options()
        options.headless = False 

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

        driver.get(self.start_url)

        # wait for category containers
        category_divs = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@class="relative flex"]')
            )
        )

        print("Total categories found:", len(category_divs))

        for div in category_divs:
            try:
                link = div.find_element(By.TAG_NAME, "a")
                name = link.text.strip()
                href = link.get_attribute("href")

                if not href or not name:
                    continue

                item = {
                    "url": href.strip(),
                    "name": name,
                }

                result = self.collection.update_one(
                    {"url": item["url"]},
                    {"$set": item},
                    upsert=True
                )

                if result.upserted_id:
                    inserted_count += 1

            except Exception as exc:
                print("Error processing category:", exc)

        print(f"New categories inserted: {inserted_count}")

        input("Press ENTER to close browser...")
        driver.quit()


if __name__ == "__main__":
    crawler = CategoryCrawler()
    crawler.crawl()
