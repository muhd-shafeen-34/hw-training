import requests
from curl_cffi import requests as curl_requests
from parsel import Selector

headers = {
    "Host": "www.bigbasket.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    #Cookie: _bb_locSrc=default; x-channel=web; _bb_aid=MjkxMzA4NDUzMA==; _bb_cid=1; _bb_vid=MTEzOTY1MTM0NjMyNzkyMDM2Ng==; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=GNNL0GlYQ7wO2s2zLnxemxPVG0QRdaqskejGdCk1a2gLP7N6hqqFaNDikdk84OQM; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; _bb_pin_code=; _bb_sa_ids=19224; _is_tobacco_enabled=1; _is_bb1.0_supported=0; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjE5MjI0; is_integrated_sa=1; is_subscribe_sa=0; bb2_enabled=true; csurftoken=zDeoSw.MTEzOTY1MTM0NjMyNzkyMDM2Ng==.1771998364229./GxQxjJ8+3DebPVdyulhIod0GzehzAoyHj5ueg28Ehc=; ts=2026-02-25%2011:24:20.555; jarvis-id=89a7729a-31e7-4f6b-a31b-0d3c2c5b7d3f; _gcl_au=1.1.260775474.1771995716; adb=0; ufi=1; _ga_FRRYG5VKHX=GS2.1.s1771995716$o1$g1$t1771998859$j59$l0$h0; _ga=GA1.2.2064446638.1771995717; bigbasket.com=a37f10dd-b685-4b19-94b7-7e3bd5889a00; _gid=GA1.2.1507038067.1771995718; _fbp=fb.1.1771995718589.84402057250333783; _gat_UA-27455376-1=1
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Priority": "u=0, i",
    "TE": "trailers",
}


api_header = {
"Host": "www.bigbasket.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
"Accept": "*/*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"X-Channel": "BB-WEB",
"Content-Type": "application/json",
"X-Tracker": "d95f4947-2b47-4fb6-9ac8-db514a869d39",
"osmos-enabled": "true",
"common-client-static-version": "101",
"X-Entry-Context": "bbnow",
"X-Entry-Context-Id": "10",
"X-Integrated-FC-Door-Visible": "false",
"Connection": "keep-alive",
"Cookie": """_bb_locSrc=default; x-channel=web; _bb_aid="MjkxMzA4NDUzMA=="; _bb_cid=1; _bb_vid=MTEzOTY1MTM0NjMyNzkyMDM2Ng==; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=GNNL0GlYQ7wO2s2zLnxemxPVG0QRdaqskejGdCk1a2gLP7N6hqqFaNDikdk84OQM; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; _bb_pin_code=; _bb_sa_ids=19224; _is_tobacco_enabled=1; _is_bb1.0_supported=0; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjE5MjI0; is_integrated_sa=1; is_subscribe_sa=0; bb2_enabled=true; jarvis-id=89a7729a-31e7-4f6b-a31b-0d3c2c5b7d3f; _gcl_au=1.1.260775474.1771995716; adb=0; ufi=1; _ga_FRRYG5VKHX=GS2.1.s1772013081$o4$g1$t1772019058$j60$l0$h0; _ga=GA1.2.2064446638.1771995717; bigbasket.com=a37f10dd-b685-4b19-94b7-7e3bd5889a00; _gid=GA1.2.1507038067.1771995718; _fbp=fb.1.1771995718589.84402057250333783; _client_version=2843; _bb_hid=7427; sessionid=mzpzcw42y06l4phxtjcto9lua3wmtlkt; _bb_tc=0; _bb_rdt="MzEwNzM5NzQwMA==.0"; _bb_rd=6; csurftoken=lQN43Q.MTEzOTY1MTM0NjMyNzkyMDM2Ng==.1772019080133.M8IL2Pkx6mwsIT4sDKNDXDOta+K5WO3KRIhpzG7BQvY=; ts=2026-02-25%2017:00:58.712; _gat_UA-27455376-1=1""",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=4",
"TE": "trailers",
}


url = "https://www.bigbasket.com/"

####################### C A T E G O R Y #################
category_tree_api_link = "https:2/product//www.bigbasket.com/ui-svc/v1/category-tree"

r1 = requests.get(category_tree_api_link,headers=api_header)
categories = r1.json()
category_links_fetch = list()
category_links_fetch.append(categories["categories"][9]["children"][0]["url"])
category_links_fetch.append(categories["categories"][9]["children"][4]["url"])
print(category_links_fetch)

###################### C R A W L E R ######################

api_url = "https://www.bigbasket.com/listing-svc/v2/products"
params = {
 
			"type": "pc",
			"slug": "coffee", #change this into tea for next url
			"page": 1
}

while True:
    respponse = requests.get(api_url,headers=api_header,params=params)
    print(respponse.status_code)
    if respponse.status_code != 200:
        break
    data = respponse.json()
    products = data["tabs"][0]["product_info"]["products"]
    for pdp in products:
        link = pdp["absolute_url"]
        id =pdp["id"]
        item = {}
        item[link] = link
        item[id] = id
    params["page"] += 1
    





#####################P A R S E R ########################


response = requests.get("https://www.bigbasket.com/pd/262799/bru-filter-coffee-green-label-500-g/?nc=l2category&t_pos_sec=1&t_pos_item=5&t_s=Filter+Coffee+-+Green+Label",headers=headers)

sel = Selector(text=response.text)
unique_id = sel.xpath('//p[contains(text(), "EAN Code")]/text()').extract_first()
product_name = sel.xpath('//h1[@class="sc-cWSHoV donMbW"]/text()').extract_first()
brand = sel.xpath('//a[@class="sc-kOPcWz jmFwda"]/text()').extract_first()

#if selling price available
regular_price = sel.xpath('//td[@class="line-through p-0"]/text()').extract_first()
selling_price = sel.xpath('//td[@class="Description___StyledTd-sc-82a36a-0 hueIJn"]/text()').extract()
#else:
regular_price = sel.xpath('//td[@class="Description___StyledTd-sc-82a36a-0 hueIJn"]/text()').extract()


breadcrumb = sel.xpath('//div[@class="Breadcrumb___StyledDiv-sc-1jdzjpl-0 dbnMCn"]//text()').extract()
product_description = sel.xpath("normalize-space(//span[text()='About the Product']/ancestor::div[contains(@class,'sc-bJBgwP')]//div[contains(@style,'font-family')])").extract_first()
storage_instruction = sel.xpath("normalize-space(//span[text()='Storage']/ancestor::div[contains(@class,'sc-bJBgwP')]//div[contains(@style,'font-family')])").extract_first()
instruction_for_use = sel.xpath("normalize-space(//span[text()='How to Use']/ancestor::div[contains(@class,'sc-bJBgwP')]//div[contains(@style,'font-family')])").extract_first()
country_of_origin = sel.xpath('//p[contains(text(), "Country Of Origin")]/text()').extract_first
nutritional_information = sel.xpath("normalize-space(//span[text()='Nutritional Facts']/ancestor::div[contains(@class,'sc-bJBgwP')]//div[contains(@style,'font-family')])").extract_first()
rating = sel.xpath('//span[@class="Label-sc-15v1nk5-0 sc-kOHTFB jnBJRV kxjCtF sc-eBMEME emPkPc"]//span[@class="Label-sc-15v1nk5-0 jnBJRV"]/text()').extract_first()
review = sel.xpath('//div[@class="cursor-pointer underline text-md"]//p[@class="leading-md text-black m-0"]/text()').extract_first()
image_url = sel.xpath('//div[@class="thumbnail lg:h-94 xl:h-110.5 lg:w-17 xl:w-21"]//@src').extract()
features = sel.xpath("normalize-space(//span[text()='Features']/ancestor::div[contains(@class,'sc-bJBgwP')]//div[contains(@style,'font-family')])").extract_first()
manufacturer = sel.xpath('//p[contains(text(), "Manufacturer Name & Address")]/text()').extract_first()
ingredients = sel.xpath("normalize-space(//span[text()='Ingredients']/ancestor::div[contains(@class,'sc-bJBgwP')]//div[contains(@style,'font-family')])").extract_first()
instock = sel.xpath('//button[@class="Button-sc-1dr2sn8-0 sc-jGKxIK dEdziT kCeaPI"]/text()').extract_first()
