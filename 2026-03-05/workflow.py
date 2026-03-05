from curl_cffi import requests
from parsel import Selector
import json

header = {
    "Host": "bens-appliances.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://bens-appliances.com/",
"Connection": "keep-alive",
"Cookie": "localization=IN; cart_currency=INR; _shopify_y=26995a7b-20f4-48ef-8a6e-4c9b2fc01786; _shopify_s=e9159a72-23fc-428f-a80a-8f8d4a762764; _shopify_essential=:AZy8Sb80AAEAluzIVCP0EYrktRwacGvOaqS1CtiPpkKmKPM9vh-eqRgVsjDDFB23VQfqPVBuey_4DM9Bs88kK5F72nMlO6BFQSpkoW0EYVPDwhmNkoY_50acqkc_5jWfH4cm9y9WdU1KjJE6Lax_Hea-WdCi2Esa2c9nfxIiCFpCq1FxA_5odR3UBSp2LvsFbvvT_5dOR-EON-O3thXVq0BYtGP1LDNA7Ue7v0SdR8kQUBimlPK8EeinrxsfW9N-7SYkcCM7UQCDGhx9U-vkjpJozWggJxtEGLUJIFSShGn2G7maSj-60-A18io7oeFQSHFuwPD3Jj8NJL2h074BuNV_YIAnCOjlQu1XFMiVT_WnLseg8516WShRJnZ23Ws7OXCH0_EYouPMs7qhXzDkqqTvnBej5CWX2ORTItxzvg:; _shopify_analytics=:AZy8ScDXAAEA-ZbtdoovSNIx_pIm09XOEyFtdo4aWmpZNZ0fcgIb4Dm2-ZGaCzZfk6OeQZSr6jxB_Em0JEWwZvFCeMw:; _ga_DCFNY9E0XR=GS2.1.s1772685480$o1$g1$t1772687555$j45$l0$h0; _ga=GA1.1.1193578771.1772685481; _ga_Z1RVEG15EB=GS2.1.s1772685479$o1$g1$t1772687555$j45$l0$h0; _ga_79LJR1R713=GS2.1.s1772685480$o1$g1$t1772687555$j45$l0$h0; _ga_V7N0GGJLMB=GS2.1.s1772685480$o1$g1$t1772687640$j59$l0$h0; _ga_L8K02GV0WK=GS2.1.s1772685480$o1$g1$t1772687640$j26$l0$h0; _gid=GA1.2.1127470842.1772685481; _ttp=01KJY4KQ049CA87RW6FQSJRW27_.tt.0; ttcsid_D3RQL7JC77U4FIU0R4GG=1772685483019::Afj9SVu1LzjnYZoLqJxu.1.1772687556712.0; ttcsid=1772685483020::jDZk4F2eaRKPUIiweqYz.1.1772687556716.0; _fbp=fb.1.1772685483221.951173941873322768; lo-uid=c866c4ab-1772685485626-1eb414c4fa488317; lo-visits=2",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"If-None-Match": "page_cache:57580716190:CollectionDetailsController:a8320f608bdee467b2880678ea419f61",
"Priority": "u=0,i",
}


oem_header = {
"Host": "oemparts.bens-appliances.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://oemparts.bens-appliances.com/products/air-handler-housing-kit-fdbm",
"Connection": "keep-alive",
"Cookie":""" _shopify_y=26995a7b-20f4-48ef-8a6e-4c9b2fc01786; _shopify_s=e9159a72-23fc-428f-a80a-8f8d4a762764; _ga_DCFNY9E0XR=GS2.1.s1772685480$o1$g1$t1772703670$j58$l0$h0; _ga=GA1.1.1193578771.1772685481; _ga_Z1RVEG15EB=GS2.1.s1772685479$o1$g1$t1772703669$j59$l0$h0; _ga_79LJR1R713=GS2.1.s1772685480$o1$g1$t1772703669$j59$l0$h0; _ga_V7N0GGJLMB=GS2.1.s1772685480$o1$g1$t1772704074$j55$l0$h0; _ga_L8K02GV0WK=GS2.1.s1772685480$o1$g1$t1772704074$j55$l0$h0; _gid=GA1.2.1127470842.1772685481; _ttp=01KJY4KQ049CA87RW6FQSJRW27_.tt.0; ttcsid_D3RQL7JC77U4FIU0R4GG=1772685483019::Afj9SVu1LzjnYZoLqJxu.1.1772703671581.0; ttcsid=1772685483020::jDZk4F2eaRKPUIiweqYz.1.1772703671584.0; _fbp=fb.1.1772685483221.951173941873322768; lo-uid=c866c4ab-1772685485626-1eb414c4fa488317; lo-visits=15; localization=US; cart_currency=USD; _shopify_essential=:AZy8ZlA1AAEArLqbQTZz9m4R2qcgH-KJTeCeNWtPnZzoDTYg3_7qREMwFDjq9EczipGN1FfhMbu2ncpP_HYHXp0eNiyj_f9oSqgWq5w5iO1Fr0yMRRIPGJ4bFzVw4ygZ6rMxDO9zIeyiCcfhzH2sD-ZOeIzrp9OCaOKlORJd0syWUct6zKQihg6rj7evmygoaJHY52QMQv9HgPRR0PCY_GfxEP9avKtrbl3_1zFrED5mFNO622-v26nF3WK3pR4yFi_HemvpUywaKwG4M5xdDJUNc29TakjpCmOxEwYTuc7YJo0GxqN-hji_o-8A0EN9KSw0xZzYsdZaQnLu6pHnfkl3EP9XPfWC2p0JSSkrfVjqgtMDFqrPKZKBZ6MQWIJJI-vWbMyzsy8DgK24MV7DyvApzxa2Qt-thyCdP8QwUV0554x1sskcm39O43nfTh-PM2gR3oiOWB5UH_bdJmU:; _shopify_analytics=:AZy8ZlGhAAEAejRCrpWO1h5UpS5DvlxZWxtBx6pn817l-nQQlOsQzR7MzhSNwBYXbweID1kUIoUukhR_PnLHCyk4sEzBncEgWul7QtQm88LI-wt1ArhgHsNYFMwXh5t8_SZ1WsakRdIZ-7I:; cart=hWN9UDuNNzh6XV3gBmcIBr2i%3Fkey%3De5df1b7c0c190d4f522930a9ce5f600e""",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"If-None-Match": "page_cache:72328970554:BuiltInCollectionDetailsController:82c3997342daa26105526d8f0e072c60",
"Priority": "u=0, i",
"TE": "trailers",
}



####### C R A W L  E R ###################

url = "https://bens-appliances.com/collections/all"
response = requests.get(url,headers=header)
print(response.status_code)
html = response.text
selector = Selector(text=html)
pageno = 1

api_url = f"{url}/?page_{pageno}"
while True:
    response = requests.get(api_url,headers=header)
    is_next = parse_item(response)
    if not is_next:
        break

    pageno += 1
    api_url = f"{url}?page_{pageno}"

##### X P A T H #########
PRODUCT_CARDS = './/div[@class="product-item product-item--vertical   1/3--tablet-and-up 1/4--desk"]'

PRODUCT_LINK = './/a[@class="product-item__title text--strong link"]/@href'
CRAWLER_PDP_NAME_XPATH = './/a[@class="product-item__title text--strong link"]//text()'
CRAWLER_PDP_PRICE_XPATH = './/div[@class="product-item__price-list price-list"]/span/text()'
CRAWLER_PDP_MANUFACTURER = './/a[@class="product-item__vendor link"]/text()'




######### P A R S E R #####################
url = "https://oemparts.bens-appliances.com/products/air-handler-housing-kit-fdbm"
response = requests.get(url,headers=header)
print(response.status_code)
sel = Selector(text=response.text)
raw_json = sel.xpath('//script[@type="application/json" and @data-product-json]').extract_first()
script_data = json.loads(raw_json)
#XPATH
imput_part_number = ""
name = '//h1[@class="product-meta__title heading h1"]/text()'
brand = '//a[@class="product-meta__vendor link link--accented"]/text()'
description = '//div[@class="card__section "]//text()'
availability = '//div[@class="product-form__payment-container"]/button/text()'
compatible_product = '//h4[text()="Compatible Models"]/ancestor::div[1]/following-sibling::div//a/text()'
equavalent_part_numbers = '//ul[@class="modelnos"]/li/a/text()'
image_urls = script_data["product"]["images"]
#need to clean image_urls