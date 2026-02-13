import parsel as pq
import re
from curl_cffi import requests 
header = {
     
     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
     "Accept-Encoding":"gzip, deflate, br, zstd",

    "Accept-Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",

   "Host":"www.academy.com",
    "Referer":"https://www.academy.com/c/mens?&facet=%27facet_Price%27:%3E%20500",
    "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
}  









########################### P A R S E R ########################################

response = requests.get(url= "https://www.academy.com/p/bcg-mens-performance-fleece-tapered-pants?sku=black-x-large",
                headers = header, impersonate="chrome120")
print(response.status_code)

html = response.text
selector = pq.Selector(text=html)

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
specification =selector.xpath('//div[@class="textBodyLg content--Ga7_8"]/ul//text()').extract()


