import requests as rq
import parsel as pq
import csv
import tls_client
import hrequests
from lxml import html
import re
import time
from urllib.parse import urljoin
import json
from pymongo import MongoClient
import logging
from pathlib import Path

############## C O N F I G ###########################

INDEX_PAGE_URL = "https://www2.hm.com/en_in/index.html"
LISTING_API_URL = "https://api.hm.com/search-services/v1/en_in/listing/resultpage"

DOMAIN = "https://www2.hm.com"

HEADER = {
    "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Host": "www2.hm.com",
    "Priority": "u=0, i",
    "Sec-Fetch-Mode": "navigate",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www2.hm.com/en_in/index.html",
    "Cookie": """bm_s=YAAQz0vSF/8to9ybAQAA7O3SAQRcehdMARRWY4Wbhpgz46YbNeSVc/ZqQGxh41/5FXrmlAOf4G/+yqoXq1Ok81qgkAhRvu5XAbad0gWi4KbuIL8ln9FkSFcqv1l4QcqNOGA0vAm23CBu1DUQbPX2rzkM/MTESQjvFV7shIux4pklOJacGZjErtm8U2+q8tUZCo0+gzDkNs2KdsSDr90X8rJp/f9ZM592GWSGtGewhQxCeNPiVEI3ZYS+u5cf1p1/6lrwZACQKOcB8I3nuXPkpRooseNIJh7HqddJ4DXgiTw+j1CogpACFGotmIRdeoxwmByF8EaHn0IUJyee1VqUlnu5qsjilPTgd0CHC7Kzj4vhSZhbonQb7PGG8nuStBx4S5Ybp/wy6NNEQa5iyKDeiUghtkE3dQxZJdT9Mj2LscerdKH5YDM7Li7HID8ztDzNY9VqRfe4FTr+AMLJmMY8TXfBdaqc4DhENEHGGQ8nvqt4r3jZsM7vDkqsDaTLuvqrxPbgyL/dOBt/YU7nZ+XYjfqyN/KFwDy8o4VKZYLiXFAQX90KIqaErRjElMOqHpZrzGVFhEhouQbt19DWXKn9; bm_so=DAD4452268A0EAA7A7345706E02A814330D5556A06F243A2B903D0932F048A47~YAAQz0vSF+Ato9ybAQAAG9fSAQYIazkIv6H/xMJwSyllhy9Iit9Pn+N9mOcj+mHxRyehy+ORqld1723neZOe4fVb14xhhhJnupyq3KvGl8AE+KBVzi6XPPsNXfKhD0R9EJU+QnH2Sa4raQW5GPdGA79FtRmiwnP1sYwHeRakqR+Fr3lrJQofEqJhWHxlvvVFtlsgYAr9qHS+VoBMV8odcnKPnjdep4ixExMPjsVjL+e2l1IpxTskeqgZmdQEx5WXjw5OJN6cDUcSGnww2+RcRgwKRnUNVCQPt+6Uxn43AttprsXwgYemxsCCFLl6aznYIURub8NNJPg7cOEavLo6p4snmfuyl/CuUKGgL8DO7/c/lA9dy6jp8NArX0n2KlybNXDNurFOFNN67YCMe9dxctvn4wqdDbXW5Dlt6G6P0QUegsEUR3G9yMBXfD7DYwNYNZe7EF4qa0tKVmAL; hmid=1408110B-B1EE-49D3-897D-D1B2D08F29DD; bm_lso=DAD4452268A0EAA7A7345706E02A814330D5556A06F243A2B903D0932F048A47~YAAQz0vSF+Ato9ybAQAAG9fSAQYIazkIv6H/xMJwSyllhy9Iit9Pn+N9mOcj+mHxRyehy+ORqld1723neZOe4fVb14xhhhJnupyq3KvGl8AE+KBVzi6XPPsNXfKhD0R9EJU+QnH2Sa4raQW5GPdGA79FtRmiwnP1sYwHeRakqR+Fr3lrJQofEqJhWHxlvvVFtlsgYAr9qHS+VoBMV8odcnKPnjdep4ixExMPjsVjL+e2l1IpxTskeqgZmdQEx5WXjw5OJN6cDUcSGnww2+RcRgwKRnUNVCQPt+6Uxn43AttprsXwgYemxsCCFLl6aznYIURub8NNJPg7cOEavLo6p4snmfuyl/CuUKGgL8DO7/c/lA9dy6jp8NArX0n2KlybNXDNurFOFNN67YCMe9dxctvn4wqdDbXW5Dlt6G6P0QUegsEUR3G9yMBXfD7DYwNYNZe7EF4qa0tKVmAL~1769557121354; utag_main__sn=30; RT="z=1&dm=hm.com&si=df09a1f5-4dcc-428f-baad-88310059d0f5&ss=mkx7yet8&sl=2&tt=69s&bcn=%2F%2F684d0d45.akstat.io%2F&ld=o2i4"; hmgroup_consent=datestamp=2026-01-22T10:10:17.890Z&url=https://www2.hm.com/en_in/index.html&consentId=800d4e50-c2a4-41b5-9626-45368e5a16fb&groups=C0001:1,C0002:1,C0003:1,C0004:1; OptanonConsent=datestamp=2026-01-22T10:10:17.890Z&url=https://www2.hm.com/en_in/index.html&consentId=13746239-a11d-423c-ba2f-651050f9e093&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; _cs_ex=1756732829; _cs_c=0; _scid=Ep-7EpVUWUu7vkvb3afy5fikd5WHsJV9; _gcl_au=1.1.1921001708.1769076620; _ga_Z1370GPB5L=GS2.2.s1769556009$o31$g1$t1769557128$j56$l0$h0; _ga=GA1.2.1367724838.1769076620; _pin_unauth=dWlkPU1XVmtORGs0WXpJdE5UTXlNQzAwTjJOaUxXSmpaalF0TkRNMFpETmxNR1ZpTWpBeA; _tt_enable_cookie=1; _ttp=01KFJJY010X1JS41K0ST8CVFRT_.tt.1; ttcsid_C4QSSN7M5GFN4SM6UID0=1769556011712::0vDBQwJ9n3axQETkXcWd.31.1769557129387.1; ttcsid=1769556011712::ohZaobtOwpvLIk7gzY59.31.1769557129387.0; _fbp=fb.1.1769076621433.23438204642428262; _sctr=1%7C1769020200000; agCookie=731ad8e3-db51-4dc0-959a-09411a00e7e8; _abck=6E45CCF7707BF3A8EE09135495486E80~0~YAAQz0vSF/4to9ybAQAA7O3SAQ9JZzoGHcwmUIJqQSXZOP9juuYD9Uo/iDmquz/D+ZNkNk4KGQMhxHp1qlZWXy1G9NtxL2lC4nwkPvbgj3zCclEPdXW2zrMjsj9deqcZ4+xpfLICoIw3pZdksglcBVa7NDvpQYft2TllMkMeaRA55bnKZk3mdxg/MLhC6kzlubZEajvfRpoWgiSlVD0zOR90KswYb9imiki0V7ZCGW68FoikW+kGePSagmARIy2cIVzEDYOSHBtGC3MzToG0KjZJzVbBIMIg2k69qmRLKw793ylnN8jaADTemnVriVnQ4AO0A35TAR0Ic0635ghTITR+yOLFK4p+aGcLZ5+nbr7vyjkjiVvmh29RzcTPPuoG200PY/CRFbHSmooQgMb4rVYnf1l3fAJn/AXAEzkRn5bgCHSGByrcosBBrnfq1lD7gukT1eWKGdINWGvhL7DwTHeJyLYqGpG//ANsxMjRVi7Tk+BudmXeljJoVPhoylfH+KY4FMknMumIMJYUHBRBUXR4olKIsA5pxN4zg4AsAA5fBB/mAV5QkCfqXcmH8lHJGblO6NIDDNbc3mXbSg91dV6TikWN+zZTvyQzY2bppdAO8hnaJCOX0sTTxnKOLjC2zU+o368Upcyb3fKRgvm3qjn6ESLzBUexJ3fdzuiD0lDMCirA6KYHMC58iagdIkJTlEdgU6yZnhrvQQ4wqxZfZX2/YmGdM1n4wvucIwWrUZLq5neALRM5yQ==~-1~-1~1769557265~AAQAAAAF%2f%2f%2f%2f%2f+YEXFOhCyWwFYaf6rAfeDudPa9Bc%2fMRxDOckotQQZ2esWXLuzBFNsGsv%2f3gG86oWxOwQexTccDbTCgoPZ5EA6%2fwL0wcMGPT0Up7XCSu9cc9cZ+%2fNNr599KtlJx1XXYEL%2fwDNaxvtvHh4qLpmNtKFOXQWUEbbrd6HbFU%2fo2I4IRpFen1pUxxm9m9bUTAeZRuXAKbiRVONygrV4+Pr6gCRZdB2J4YyC5TDfFCuXNN182lvMw%3d~-1; hm-india-cart=17209be6-cbb9-45f8-b42a-bcb6b4a9a3d2; HMCORP_locale_autoassigned=false; HMCORP_locale=en_IN; HMCOUNTRY_name=India; hm-india-favourites=""; bm_sz=B54F4D8ECE375DD0B140E8DABE65ACD8~YAAQz0vSF+0to9ybAQAAHOTSAR78zR38Gi+5JSdcZVnXJz4IxY7ffBonnmuKvXu0M5AdSrXvXnUvY2VckqxMTgwm8RzjGYMGtSYivbLZZDj/fq59+Hvq+Ngbly8cwfARHWYx7/rl7B334TGuowWYaBX4Y05YgHtUsE+DDdGRPSeutBXBKr7nN0Eklk6FK5qQS8MTuve246br57q+mIZdnC+zPY7Q+z0Fo4fTqhtHrFL4yfscOnIgqLX9V3EqtFZSEmXpoAPHJJ0imQ/ckBU5L40a9DVxHIC46u0XW0OVfZlFzOaFrhFcHDo4ACGMH8DALFBjk7/TmSLbQ90uvO7/IOOu0AgxgpjDhyPDgVDdRKCWENIElL4+Z+sn54en82BpYzkc2P6chwLw8PQ9AdWRPtaIhhGpsKi5DUWlzLIumCra1eBgApaMOo+369Fjbquac30wwBqxm4VoOJiHkdwmwMfEuH1aTSDSPSLe/PYWAowFwU3FPxolEzSgdEhUrhf4kZUTwoHWPt+Le9cxb/RVtFUXCFoNMHyNfQt7p7tkaiCjv1UecRvFPPR9q5MZqZnfP9c4y3fGRQ==~3683137~3422518; akainst=APAC; akavpau_www2_en_in=1769557426~id=4ceaea0bce9af17582d27554bddd1732; INGRESSCOOKIE=1769487594.715.402.42934|7bbf721d92a09b08c42eb8596390c8cc; JSESSIONID=EA8BBE54CDF23B4A7A7577C5C562655EE0F9013304964CDE3F15290B4E4C871ED981AA916A0A23891DEDD7D183C0A6123D1A195C609B48341B5E11A958F6D7B9.hybris-ecm-web-849ffc645b-c52gl; akamref=; OriginChoicePaymentSystem=rupay; bm_sv=DBA12B6B8353AB4ED131E9BAB45FDA86~YAAQz0vSFwAuo9ybAQAA7O3SAR5J13qHvXsR9O0/8kzryHJUz0BGJCi9PmSrtFmQ9WJOguTpF2w0MKzLW1K5SyoTmkRU//bYgxxC1zgYTf2f3JWWeoddb7sHBoSIU5soL8RpSnYsaF0nz+sr/CNUKGKWF5DBJj7Y3jE/ReEokFL4d6qV3Cy/2w7Dq/sG5rZQZvchiYQqXqgS/OXvA4nN1mafr9NYp5xq7gWhnaMdA0crXwVUJ9MBuNYWuuPT~1; AKA_A2=A; bm_ss=ab8e18ef4e; ak_bmsc=A4C0EAA16842E4058F3FA807E59C8B65~000000000000000000000000000000~YAAQh9cLF9jYZ8ebAQAAnNbBAR475RBPWhU736T9q8VjyRA+vS8rqQhlzMFXHZhFTwF2rZCWijBbDy+TE3v+fII9rR+K18bLOhcHks6VEEVbem6Qt5cZAGL2FdzIZKbNsjbGTkMpbpARQWCuN+NxpV+7+ffP11Dfnfa+cLLcazTaZV7xGQ0PRSN0G2QmQtU44LNt5CIqF5FT7XTRzCJVJLv0zijl8RizyEoC9eWmH7WRTN0Mt+bEI57B1SvqkjncnMYyrKoJB0z3Su3DGjMH9NQR2CzIZjyPbpjQCY+AVNhfZXT/ayyYEg8168a+PYupjhLfQ3iC2RlvSTvk+74TycrdHcIf94+2ZCiA28zbf428gMI+WPDSin/EAA4latw48yhkmyN1hBCAERt0fqZqJTlhJiz81PG8o570K2VuPdmFqNZ7G7FGu/rwfd5IsjwE8NPhCOUUXC8CI2Cc+UDZCYBtwBXFlUXdKMvdsPsPKvpMK7VdOIDNJlmd/NGv1j92XqVbVstP0/ZPudVonxRvMPd31Gk=; bm_mi=E3F4F833380D3F32C7D05BBD1CF92A66~YAAQh9cLF2rYZ8ebAQAA783BAR7P+00puxvhZ3RihoxYyNgljo9Nj2usCbu+027RkwYeGjkDkr4t92+1OZQf61PiC2XyPsc0LmZqpgz/vvmCMwh+v3YfuBjD8pJyOBhvzFwJF+QFg5QBBzOO8g9E7MnyWwXqumoQYKj2ij1sPSA1ejLPYQ11ciF7IJeMDts5/PoVWfp4eypWJnWoyOqC/zM7bjYfX8gJwD3J8tuaMB64TKepy45qQmAQrJcSQ2xHIFzV3lkRD1h19jNKGgNFYfVJZp4T5Wlu1qjqrR/beuZxbOrTOicbmiyvL+gTfHXZSO2rve4bvcK3Ir7/EeYPfmwytK4wr8bNvl2W9WERwfPh~1; utag_main__se=18%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__st=1769558926753%3Bexp-session; utag_main_ses_id=1769556006554%3Bexp-session; utag_main__pn=3%3Bexp-session; dep_sid=s_3940210111444952.1769556006557; dep_exp=Wed, 28 Jan 2026 00:08:46 GMT; dep_testdata=normal; userCookie=##eyJjYXJ0Q291bnQiOjB9##; _scid_r=Oh-7EpVUWUu7vkvb3afy5fikd5WHsJV9mJ8AjA; _uetsid=acadd9d0f94b11f0957f8fa9fe3cd629; _uetvid=8e971c40f77a11f0b6d8ad4d3a7ff761"""
}

################### C A T E G O R Y #####################

session = tls_client.Session(client_identifier="firefox_117")
response = session.get(INDEX_PAGE_URL,headers=HEADER)


def find_view_all_links(obj, links):
        if isinstance(obj, str):
            if obj.lower().endswith('view-all.html'):
                if "sale" not in obj.lower() and "new-arrivals" not in obj.lower():
                    links.add(obj)
        elif isinstance(obj, dict):
            for value in obj.values():
                find_view_all_links(value, links)
        elif isinstance(obj, list):
            for item in obj:
                find_view_all_links(item, links)

category__view_all_links = set()
tree = html.fromstring(response.content)
script = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')
for i in script:
    data = json.loads(i)
    find_view_all_links(data,category__view_all_links)

############## C R A W L E R ###############################

session = tls_client.Session(client_identifier="chrome_120")
response = session.get(url="https://www2.hm.com/en_in/men/shop-by-product/view-all.html",
                       headers=HEADER)

def find_key_recursive(self,data, target_key):
    # """Yields all values for a specific key in a nested structure."""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    yield value
                else:
                    yield from self._find_key_recursive(value, target_key)
        elif isinstance(data, list):
            for item in data:
                yield from self._find_key_recursive(item, target_key)


tree = html.fromstring(response.content)
script = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]
data = json.loads(script)
pageId = list(find_key_recursive(data,"pageId"))[0]
categoryId = list(find_key_recursive(data,"tagCodes"))[0]

PARAMS = {
            "pageSource": "PLP",
            "page": 1,
            "sort": "RELEVANCE",
            "pageId": pageId,
            "page-size": "36",
            "categoryId": categoryId,
            "filters": "sale:false||oldSale:false",
            "touchPoint": "DESKTOP",
            "skipStockCheck": "false"
                        }

response = session.get(url=LISTING_API_URL,headers=HEADER,params=PARAMS)
list_of_pdp_urls = list()
data = response.json()
products = data["plpList"]["productList"]
for i in products:
    url = i.get("url")
    print(url)
    list_of_pdp_urls.append(url)                        
    PARAMS["page"] += 1

################### P A R S E R ##############################

for pdp_url in list_of_pdp_urls:
    product_url = urljoin(DOMAIN,pdp_url)

    product_response = session.get(product_url,headers=HEADER)
    

    html = product_response.text
    selector = pq.Selector(text=html)
    prod_url = product_response.url
    breadcrumbs_fetched = selector.xpath('//ol[@class="b43307 ea1998"]//text()').getall()
    breadcrumbs = "".join(breadcrumbs_fetched)
    Title = selector.xpath('//h1[@class="b9e19c c779b4 b44f77"]//text()').get()
    selling_price_fetched = selector.xpath('//span[@data-testid="red-price"]//text()').get()
    regular_price_fetched = selector.xpath('//span[@data-testid="line-through-white-price"]//text()').get()
    Description = selector.xpath('//p[@class="fdb3e1 cfeb83 b493f8"]//text()').get()
    Net_quantity = selector.xpath('//dd[@data-testid="description-netQuantityAccordions"]/text()').get()
    fit = selector.xpath('//dd[@data-testid="description-fits"]/text()').get()
    country_of_origin = selector.xpath('//dd[@data-testid="description-countryOfProduction"]//text()').get()
    diamentions= selector.xpath('//dd[@class="fdb3e1 cfeb83 f1bad1 acddb1"]//text()').getall()
    fabric_composition = selector.xpath('//li[@class="b819ff"]//text()').getall()
    care_instructions = selector.xpath('//ul[@class="e00dc3"]//text()').getall()
    model_fit = selector.xpath('//dd[@data-testid="description-modelHeightGarmentSize"]//text()').get()



################ F I N D I N G S ##################################


#1. API Pagination : methods and its parmeters sending with requests
#2. Hydration data : this website hydrate data on client side and it contains all the api parameters