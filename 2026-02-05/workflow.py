import requests as rq
import parsel as pq
from urllib.parse import urljoin

####### C O N F I G ########
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    # 'Cookie': 'pz-locale=en-ae; pz-currency=aed; _gcl_au=1.1.1480680565.1770102131; _ga_DR0EDZPL9N=GS2.1.s1770180426$o4$g1$t1770181725$j59$l0$h1558101284; _ga=GA1.1.664013350.1770102132; _ga_XK00CLKQ26=GS2.1.s1770180426$o4$g1$t1770181725$j59$l0$h0; theme=scheduled; cf_clearance=uYsD_yShxW6tDOACBRbOn4KuVxaDLt6AfHtkfCQwldc-1770181174-1.2.1.1-ZnGIEHk0jPWf1AY9M8dItSiYy6emLEmchrGkUd_ePvIVJW2fBJLdXU7nEQrTVGA8vEG991zeN7CmhU0CLaWQLotyEdilQ.3vjA1vLojkWkLN_7.DMqB1Ca9APjO3RfokU12I6DFIiTPBDqz.IQocoMc8hID7_kp3yPuKvZVWLOgCLxtoYt1A_OD8D.ul3J0NDqbgpGSY8g7eXZz9RIu9uO6YJ3.E6hYFIF4eyp17y7Y; _fbp=fb.1.1770102134758.434562169552980789; _tt_enable_cookie=1; _ttp=01KGH4Y62TPAVZN406V29ZKN7A_.tt.1; ttcsid_C43T0KUI9NESIEHLOAL0=1770180429900::aRPJdDDf-GumHRGYwh6T.3.1770181727060.1; ttcsid=1770180429901::lTuqdjv-GSO6ob4hEayQ.3.1770181727060.0; _scid=2-Dt9NTZho2noMRytmMbdMv1qXgDVuHP; _sctr=1%7C1770057000000; csrftoken=tBCkA1AW5IyB7pk3bUJzdzXfJilj4Rnaw0BQskwQOfqz8BufNHwD88O4WFFqgVw4; __cf_bm=tdh5Ijs.Y7wlMkrLRPhkgyBtOreP5roBYe35FWYr37U-1770181726.1783297-1.0.1.1-NvFPQtVtHt5SsBOjNph2Y_lLspd69zLi1EIO4yBbuetbbdPwoERyaboF_CuCBHqPQHQYRGFVEGZvrunwfaF.f5NRV_x60PlUXe9x7IYqcwXQblAz000_U2f2u8DFxVfM; pz-frontend-id=1; __Host-next-auth.csrf-token=ca2370ab9866a1fd14d1acc779909b4f42fd55560205e6d4f3e27c0a01129dec%7Ce3030769ad8cbc15f70bec266ac6e7a925464a9dfd8e805cf694296c4fd33913; __Secure-next-auth.callback-url=https%3A%2F%2Fgcc.luluhypermarket.com%2Fen-ae; userLocationWeb={"country":"UAE","locationTitle":"Al Nahyan","latitude":24.4351413,"longitude":54.4120335,"ffc":"2480"}; xxx111otrckid=8ae6897b-0667-4136-9db7-ce0a20207416; _scid_r=6WDt9NTZho2noMRytmMbdMv1qXgDVuHPcVsouA',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Priority': 'u=0, i',
}

DOMAIN = "https://gcc.luluhypermarket.com/en-ae"
CATEGORY_API = ""

######### C A T E G O R Y ############################




############# C R A W L E R ######################
current_url = "https://gcc.luluhypermarket.com/en-ae/grocery-food-cupboard/"
while current_url:
    response = rq.get(url=current_url,headers=HEADER)
    html = response.text
    selector = pq.Selector(text=html)

    plp_links = []

    plp_links_fetch_xpath = selector.xpath('//a[contains(@class,"relative") and contains(@class,"flex") and contains(@class,"flex-col")]/@href').extract()
    next_page = selector.xpath('//a[@class="flex cursor-pointer px-2 text-xs"]/@href').extract_first()
    if next_page:
        current_url = urljoin(current_url,next_page)
    else:
        break


############ P  A R S E R ##############################

pdp_url = "https://gcc.luluhypermarket.com/en-ae/barakat-fresh-green-juice-330-ml/p/1295005/"

response = rq.get(url=pdp_url,headers=HEADER)
html = response.text
selector = pq.Selector(text=html)

title = selector.xpath('//h1[@data-testid="product-name"]/text()').extract_first()
regular_price_fetch = selector.xpath('//span[@data-testid="price"]/text()').extract_first()
regular_price = f"{float(regular_price_fetch):.2f}"

brand = selector.xpath('//a[@class="whitespace-nowrap text-primary"]/text()').extract_first()
description = selector.xpath('//ul[@class="space-y-3.5"]//text()').extract()
if description:
    description_full = ",".join(description)
else:
    description=""

#################### FINDINGS ###############################

#Category links are available on API