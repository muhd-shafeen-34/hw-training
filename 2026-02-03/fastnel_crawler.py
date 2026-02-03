import time
import requests as rq
from urllib.parse import urljoin
import settings

class Crawler:
    def __init__(self):
        self.session = rq.Session()
        self.session.headers.update(settings.HEADERS)
        self.list_of_pdp_urls = []

    def crawl_products(self, category_data):
        """
        Paginates through product listings for a single category dictionary.
        """
        # Extract initial payload and name from data which gets from mongodb
        payload = category_data.get("payload", {}).copy()
        category_name = category_data.get("name", "Unknown Category")
        
        # Start pagination from page 1
        page_num = 1
        
        while True:
            # Update the payload with the current page number
            payload["page"] = str(page_num)
            payload["pageSize"] = "12"
            
            print(f"Requesting Page {page_num} for {category_name}")
            
            try:
                response = self.session.post(
                    settings.API_URL, 
                    json=payload, 
                    timeout=15
                )
                
                if response.status_code != 200:
                    print(f"Stop: Received Status {response.status_code}")
                    break

                data = response.json()
                products = data.get("productList", [])

                # Break if no products are returned (End of Category)
                if not products or not isinstance(products, list):
                    print(f"End of results reached at page {page_num}.")
                    break

                for item in products:
                    sku = item.get("sku", "")
                    pdp_entry = {
                        "name": item.get("description") or item.get("mp_des"),
                        "sku": sku,
                        "url": urljoin(settings.DOMAIN, f"/product/details/{sku}"),
                        "payload": {
                            "attributeFilters": {},
                            "pageUrl": f"/product/details/{sku}",
                            "productDetails": True,
                            "sku": [sku]
                        }
                    }
                    print(f"Found SKU: {sku}")
                    self.list_of_pdp_urls.append(pdp_entry)

            
                page_num += 1
                
                # sleep for checking values
                time.sleep(1.5)

            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def save_results(self):
        """Saves the collected PDP payloads back to Mongo."""
        if self.list_of_pdp_urls:
            print(f"Saving {len(self.list_of_pdp_urls)} items to MongoDB...")
            settings.save_to_mongo(self.list_of_pdp_urls,"pdp_links")

if __name__ == "__main__":
    # 1. Get that single dictionary from your settings helper
    listing_page = settings.fetch_from_mongo("category_links")
    
    if listing_page and isinstance(listing_page, dict):
        crawler = Crawler()
        crawler.crawl_products(listing_page)
        crawler.save_results()
    else:
        print("No category data found in MongoDB.")



