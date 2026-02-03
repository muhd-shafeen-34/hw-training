import requests as rq
from urllib.parse import quote, urljoin
import settings
from pymongo import MongoClient, UpdateOne

class CategoryCrawler:
    def __init__(self):
        self.session = rq.Session()
        self.session.headers.update(settings.HEADERS)
        self.listing_page_links = []
        # Track IDs to prevent infinite loops
        self.seen_ids = set()

    def fetch_data(self, payload):
        """Performs the POST request and returns JSON."""
        try:
            response = self.session.post(
                settings.API_URL, 
                json=payload, 
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            print(f"Error {response.status_code} for URL: {payload.get('pageUrl')}")
        except Exception as e:
            print(f"Request failed: {e}")
        return None

    def get_level_name(self, item):
        """Determines the name of the category regardless of level depth."""
        for key in ["categoryLevelFour", "categoryLevelThree", 
                    "categoryLevelTwo", "categoryLevelOne"]:
            if item.get(key):
                return item.get(key)
        return "Unknown"

    def crawl(self, payload, depth=1):
        """Recursive function to traverse category levels with loop protection."""
        current_id = payload.get("categoryId")
        
        # 1. Stop if we've already processed this ID
        if current_id in self.seen_ids:
            return
        self.seen_ids.add(current_id)

        print(f"Crawling Level {depth}: {payload.get('pageUrl')} (ID: {current_id})")
        data = self.fetch_data(payload)
        
        if not data:
            return

        categories = data if isinstance(data, list) else data.get("categoryList", [])

        # 2. If no categories, or the API just returned the current category back to us
        if not categories or (len(categories) == 1 and categories[0].get("categoryId") == current_id):
            self.save_link(payload)
            return

        for item in categories:
            new_id = item.get("categoryId")
            
            # Skip if sub-category is the same as parent (API loop)
            if new_id == current_id:
                continue

            if item.get("familyId"):
                leaf_payload = payload.copy()
                leaf_payload.update({
                    "categoryId": new_id,
                    "familyId": item.get("familyId")
                })
                self.save_link(leaf_payload)
                continue

            # Construct next payload
            next_payload = {
                "attributeFilters": {},
                "categoryId": new_id,
                "categoryLevelOne": item.get("categoryLevelOne", ""),
                "categoryLevelTwo": item.get("categoryLevelTwo", ""),
                "categoryLevelThree": item.get("categoryLevelThree", ""),
                "categoryLevelFour": item.get("categoryLevelFour", ""),
            }
            
            next_payload = {k: v for k, v in next_payload.items() if v}
            
            # Construct nested Page URL
            path_parts = [
                item.get("categoryLevelOne"),
                item.get("categoryLevelTwo"),
                item.get("categoryLevelThree"),
                item.get("categoryLevelFour")
            ]
            valid_parts = [quote(str(p)) for p in path_parts if p]
            next_payload["pageUrl"] = f"/product/{'/'.join(valid_parts)}"

            self.crawl(next_payload, depth + 1)
        settings.save_to_mongo(self.listing_page_links,"category_links")

    def save_link(self, payload):
        """Formats and stores the final listing URL."""
        name = self.get_level_name(payload)
        params = f"?categoryId={payload['categoryId']}"
        if payload.get("familyId"):
            params += f"&productFamilyId={payload['familyId']}"
            
        full_url = urljoin(settings.DOMAIN, payload["pageUrl"]) + params
        
        # Check if already saved to avoid duplicates in the list
        if any(link['url'] == full_url for link in self.listing_page_links):
            return

        final_payload = payload.copy()
        final_payload.update({"page": "1", "pageSize": "12"})
        final_data = {
            "name": name,
            "url": full_url,
            "payload": final_payload
        }
        print(final_data)
        self.listing_page_links.append(final_data)
        print(f"Saved: {name}")
    

if __name__ == "__main__":
    crawler = CategoryCrawler()
    initial_payload = {
        "categoryLevelOne": settings.ROOT_CATEGORY,
        "categoryId": settings.ROOT_CATEGORY_ID,
        "attributeFilters": {},
        "pageUrl": f"/product/{settings.ROOT_CATEGORY}"
    }
    crawler.crawl(initial_payload)