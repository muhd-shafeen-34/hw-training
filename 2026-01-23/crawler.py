import requests
import tls_client
from settings import HEADER, PARAMS, URL


class Crawler():

    def __init__(self):

        self.session = tls_client.Session(client_identifier="chrome120")
        self.plp_url = URL
        self.list_of_pdp_urls = []


    def crawl(self):
        
        while True:
            response = self.session.get(self.plp_url,headers=HEADER,params=PARAMS)
            print(f"[INFO] STATUS CODE FOR PAGE NO : {PARAMS["page"]} = {response.status_code}")

            if response.status_code != 200:
                print("[ERROR] Request blocked or failed")
                break
        
            try:
                data = response.json()
            except Exception as e:
                print(f"Cookie Expired or {e}")
            products = data["plpList"]["productList"]

            if products:
                print(f"[INFO] Fetching product urls from Page no: {PARAMS['page']} ")
                count = 0
                for i in products:
                    url = i.get("url")
                    if url:
                        print(url)
                        self.list_of_pdp_urls.append(url)
                        count += 1
                print(f"[INFO] Fetched {count} urls from page no {PARAMS["page"]}")
                print("****************************************************************")
                PARAMS["page"] += 1

            else:
                print("[INFO] No more products Reached last page")
                break

        return self.list_of_pdp_urls
