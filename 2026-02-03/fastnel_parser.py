import time
import requests as rq
from urllib.parse import urljoin
import settings
import re
class Parser:
    def __init__(self):
        self.session = rq.Session()
        self.session.headers.update(settings.HEADERS)
        self.pdp_data = []

    def get_breadcrumb_path(self, breadcrumbs):
        """Extracts human-readable labels and joins them into a path."""
        if not breadcrumbs:
            return ""
        
        levels = [
            breadcrumbs.get("mp_categoryLevelOneLabel"),
            breadcrumbs.get("mp_categoryLevelTwoLabel"),
            breadcrumbs.get("mp_categoryLevelThreeLabel"),
            breadcrumbs.get("mp_categoryLevelFourLabel"),
        ]
        return " > ".join(filter(None, levels))

    def parse_pdp(self, item_doc):
        """Handles the API request and parses the complex JSON response."""
        payload = item_doc.get("payload", "")
        url = item_doc.get("url", "")

        try:
            response = self.session.post(settings.API_URL, json=payload, timeout=15)
            if response.status_code != 200:
                return None

            data = response.json()
            if data.get("resultType") != "productDetail":
                return None

            details = data.get("productDetail", {})
            breadcrumbs = data.get("breadCrumbs", {})

            # 1. Basic Info
            imageurls = details.get("allImages",[])
            price_list = details.get("pdd", [])
            if price_list:
                price = price_list[0].get("pr", "")
                package_size = price_list[0].get("mp_uom", "")
                package_size_fetch = re.findall(r'\d+', package_size)
                if package_size_fetch:
                    package_size_of_price = package_size_fetch[0]
                else:
                    package_size_of_price = ""
         
                if len(price_list) > 1:
                    price_per_unit_fetch = price_list[1].get("pr", "")
                    price_per_unit = price_per_unit_fetch if price_per_unit_fetch else ""
                else:
                    price_per_unit = price
            else:
                price = ""
                package_size_of_price = ""
                price_per_unit = ""


            description_fetch = details.get("notes","")
            description_details = description_fetch if description_fetch else {}

            if description_details.get("mp_publicNotes",""):
                value = description_details.get("mp_publicNotes","")
                pattern = re.compile(r"<[^>]+>")
                description = pattern.sub("", value).strip()
                
            else:
                description = ""
            
            if description_details.get("mp_bulletPoints",""):
                value = description_details.get("mp_bulletPoints","")
                pattern = re.compile(r"<li>(.*?)</li>")
                items = pattern.findall(value)
                clean_list = [item.strip() for item in items]

                features = ",".join(clean_list)
            else:
                features = ""





            
            # 2. Attributes Extraction
            attr_map = {
                attr.get("mp_nm", ""): attr.get("mp_vl", "") 
                for attr in details.get("catAtt", [])
            }
            


            # 4. Final Data Construction
            return {
                "url": url,
                "image_url": imageurls,
                "breadcrumbs": self.get_breadcrumb_path(breadcrumbs),
                "title": details.get("mp_des", ""),
                "brand": details.get("brNm", ""),
                "manufacturer": details.get("mfr", ""),
                "price": price,
                "package_size_of_price":package_size_of_price,
                "price_per_unit": price_per_unit,
                "description": description,
                "features": features,
                "sku": details.get("sku", ""),
                "manufacturer_part_no": details.get("manufacturerPartNo", ""),
                "unspsc_code": details.get("unspscCode", ""),
                # Specfic Attributes
                "type": attr_map.get("Type", ""),
                "material": attr_map.get("Material", ""),
                "plate_configuration": attr_map.get("Plate Configuration",""),
                "grade": attr_map.get("Grade",""),
                "product_weight": details.get("weight",""),
                "color": attr_map.get("Color", ""),
                "overall_height": attr_map.get("Overall Height", ""),
                "overall_width": attr_map.get("Overall Width", ""),
                "number_of_gangs": attr_map.get("Number of Gangs", ""),
                # Additional Details
                "unit_of_meassurement": details.get("uom", {}).get("mp_sUOMSr", ""),
                "express_available": "Yes" if details.get("isExpress") else "No",
                "applications": description_details.get("mp_applicationUse","") if description_details.get("mp_applicationUse") else "",

            }

        except Exception as e:
            print(f"Error crawling SKU {item_doc.get('sku')}: {e}")
            return None

    def run(self, limit=None):
        """Main loop to iterate through Mongo links."""
        pdplinks = settings.fetch_pdp_from_mongo("pdp_links",limit=100)
        for i, doc in enumerate(pdplinks):
            print(f"Processing item {i+1}...")
            result = self.parse_pdp(doc)
            print(result)
            
            if result:
                self.pdp_data.append(result)
                print(f"Captured: {result['title'][:30]}...")

            

        # Bulk save at the end
        if self.pdp_data:
            settings.save_to_mongo(self.pdp_data,"fastnel_electrical_data")
            print(f"Successfully saved {len(self.pdp_data)} products.")

if __name__ == "__main__":
    crawler = Parser()
    crawler.run() # Set to None for full crawl





















