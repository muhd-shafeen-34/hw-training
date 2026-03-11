import requests

from parsel import Selector
PDP_HEADER = {
"Host": "www.delhaize.be",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://www.delhaize.be/nl/shop/Koude-en-warme-dranken/Frisdrank/c/v2DRISOF?q=%3Arelevance&sort=relevance",
"Connection":"keep-alive",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User":"?1",
"Priority": "u=0, i",
"TE": "trailers",
}

API_HEADER = {
"Host": "www.delhaize.be",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "*/*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://www.delhaize.be/nl/shop/Waters-Softdrinks-and-Fruitsap/Frisdrank/c/v2DRISOF",
"content-type": "application/json",
"apollographql-client-name": "be-dll-web-stores",
"apollographql-client-version": "e23db29dffd65300a7defc27c5ee37a4a7c75c87",
"x-apollo-operation-name": "GetCategoryProductSearch",
"x-apollo-operation-id": "841bc048e809cf7f460d0473995516d39464c46b70952bd8b26235f881f571b5",
"x-default-gql-refresh-token-disabled": "true",
"x-dtpc":"8$133198756_784h14vWKFTRODCCQWUFFHBUVARKMEDOPPOAPJC-0e0",
"tracestate":"4888dfe3-c11c5b27@dtr=1;0b01067f40b3afee;1;b0bf94df3db180f6;1773130992774SBB0ESIOD9ELEFH2O9UBONF8ISGIGCLD;EKGUUCMFPGMDKDRWWVBUKJAMNCRUHWME-0",
"traceparent":"00-4a19e37aeb1ccfbd1aad38c25604cdc4-0b01067f40b3afee-01",
"Connection": "keep-alive",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=4",
"TE":"trailers",

}





###### C R A W L E R ###############################

api = "https://www.delhaize.be/api/v1/"

variables = {
    "lang": "nl",
    "searchQuery": "",
    "category": "v2DRISOF",
    "pageNumber": 0,
    "pageSize": 20,
    "filterFlag": True,
    "fields": "PRODUCT_TILE",
    "plainChildCategories": True
}

extensions = {
    "persistedQuery": {
        "version": 1,
        "sha256Hash": "6207aa07553962b9956d475b63737d2b03b3eb7b7e6fa6ffbfc709f9894c5bdd"
    }
}

page = 0

while True:
    
    variables["pageNumber"] = page

    params = {
        "operationName": "GetCategoryProductSearch",
        "variables": json.dumps(variables),
        "extensions": json.dumps(extensions)
    }


    response = requests.get(api,headers=API_HEADER,params=params)
    print(response.status_code)
    res = response.json()
    data = res["data"]
    details = data["categoryProductSearch"]
    products = details.get("products","")
    if products:
        for pdp in products:
            link = pdp.get("url")
            id = pdp.get("code")
    

        page += 1
    else:
        break






################ P A R S E R #####################
url = "https://www.delhaize.be/nl/shop/Koude-en-warme-dranken/Frisdrank/Energiedrank/Zero-Sugar-Energiser/p/S2025042200851860099"

pdp_params = {
"operationName": "ProductDetails",
"variables": '{"productCode":"S2017082804174740099","lang":"nl"}',
"extensions": '{"persistedQuery":{"version":1,"sha256Hash":"bc98c7e3bfdca594d65bbaebb539e81887459c27c39e860f5538f05739f16236"}}'
		}

response = requests.get(url,headers=PDP_HEADER)
sel = Selector(text=response.text)
breadcrumbs = sel.xpath('//nav[@aria-label]//text()').extract()
parser_response = requests.get(api,headers=API_HEADER,params=pdp_params)
print(parser_response.status_code)
res = parser_response.json()
data = res["data"]
products_Details = data.get("productDetails","")

unique_id = products_Details["code"]
