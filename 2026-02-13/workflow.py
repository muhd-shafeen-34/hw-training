import parsel as pq
import re
import requests as rq
from curl_cffi import requests 
import settings
from urllib.parse import urljoin
header = {
     
     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
     "Accept-Encoding":"gzip, deflate, br, zstd",

    "Accept-Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",

   "Host":"www.academy.com",
    "Referer":"https://www.academy.com/c/mens?&facet=%27facet_Price%27:%3E%20500",
    "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
}  

################### C A T E G O R Y ##################################33

response = rq.get(url=settings.url,headers=settings.header)
print(response.status_code)
cat_links = []
html = response.text
selector = pq.Selector(text=html)
category_links_fetched = selector.xpath('//ul[contains(@class,"listContainer--xTWe4 bm24--S2oVK")]//@href').extract()
pattern = re.compile(r"/c/(mens|womens|kids|footwear)(/|$)")
main_category_links = [urljoin(settings.url,i)for i in category_links_fetched if pattern.search(i)] 


## sub category fetching function
def category(cat):
    response1 = rq.get(cat,headers=settings.header)
    html = response1.text
    selector = pq.Selector(text=html)
    sub1_fetch = selector.xpath('//a[@data-auid="subCategoryLinks_PLP"]//@href').extract()
    if not sub1_fetch:
        return ""
    sub1_links = [urljoin(settings.url,i) for i in sub1_fetch ]
    return sub1_links


########################### C R A W L E R ########################################


response = requests.get(url= "https://www.academy.com/c/mens/mens-apparel/mens-shirts--t-shirts/western-shirts",
                headers = header, impersonate="chrome120")
print(response.status_code)

html = response.text
selector = pq.Selector(text=html)
pageno = meta.get("pageno",1)

api_url = f"{url}?page_{pageno}"
while True:
    settings.header["Referer"] = url
    response = rq.get(api_url,headers=settings.header)
    is_next = self.parse_item(response)
    if not is_next:
        break

    pageno += 1
    api_url = f"{url}?page_{pageno}"


PRODUCTS_XPATH = '//div[@data-auid="ProductCard"]'


PDP_URL_XPATH = './/a[@data-auid="product-title"]/@href'
PDP_NAME_XPATH = './/a[@data-auid="product-title"]//text()'
PDP_RATING_XPATH = './/span[contains(@class,"ratingAvg") and contains(@class,"textCaption")]//text()'
PDP_REVIEW_COUNT_XPATH = './/a[contains(@class,"ratingCount") and contains(@class,"focusable") and contains(@class,"smallLink")]/text()'




########################### P A R S E R ########################################

response = requests.get(url= "https://www.academy.com/p/bcg-mens-performance-fleece-tapered-pants?sku=black-x-large",
                headers = header, impersonate="chrome120")
print(response.status_code)

html = response.text
selector = pq.Selector(text=html)

unique_id = selector.xpath('//div[@id="product-info"//text()]').extract()

url = response.url
product_name = selector.xpath('//h1[@data-auid="PDP_ProductName"]/text()').extract_first()
brand_name = selector.xpath('//a[@class="asoLink focusable  smallLink dNone dBlock-lg "]//text()').extract_first()

selling_price_fetch = selector.xpath('//div[@data-auid="nowPrice"]//span[@class="pricing nowPrice lg "]/text()').extract_first()
#if selling price available

regular_price_fetch = selector.xpath(('//div[@data-auid="nowPrice"]//span[@class="pricing wasPrice lg"]/text()')).extract_first()

discount_fetch = selector.xpath('//div[@data-auid="nowPrice"]//span[@class="pricing priceSaving lg"]/text()').extract_first()

#     discount_fetch_regex  = re.search(r'(\d+(?:\.\d+)?)%', discount_fetch)
#     discount = discount_fetch_regex.group(1) if discount_fetch_regex else ""

# if selling price not available

regular_price_fetch = selector.xpath('//div[@data-auid="regPrice"]/span[@class="pricing nowPrice lg"]/text()').extract_first()


description_fetch = selector.xpath('//div[contains(@class,"detailPanel--jmOfo")]//div[contains(@class,"textBodyLg")]/text()').extract_first()
# features = ""
# specification =""
image = selector.xpath('//picture/img/@src').extract()

specification = selector.xpath('//div[@class="textBodyLg content--Ga7_8"]/ul//text()').extract()



#to get color first we need unique id 
color = rf'"vendorColorName"\s*:\s*"([^"]+)".*?"itemId"\s*:\s*"{unique_id}"'

# from page source
size = r'"facet_Size"\s*:\s*\[\s*"([^"]+)"\s*\]' if shoe  r'"name"\s*:\s*"Shoe Size"\s*,\s*"value"\s*:\s*"([^"]+)"'
rating = ""#can be get from crawler
review = ""#Can get from crawler
