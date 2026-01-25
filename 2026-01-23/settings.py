import requests as rq
import parsel as pq
import csv
import tls_client
import hrequests
import re
import time
from pymongo import MongoClient


URL = "https://api.hm.com/search-services/v1/en_in/listing/resultpage"

DOMAIN = "https://www2.hm.com"

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    
    "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Host": "www2.hm.com",
    "Cookie": """bm_s=YAAQz0vSF6aFa9qbAQAAo2RB9wSXxu6vlIaFch4VhdHKZCsZo30Ug9IsvK3OsY0yyuatVZdTclXKS/QDsaK06t2aQgJTosi6ljVS4GI9rXKy32ngYza5Y45iAu+jcX1cFAajPSqcrDWIKM6Ge+L3OVhJGASGEuJfEFQSYdGczDUy3kUCpSXDA1E/UpzM+euFisJHlTiZLKhimTCzoDtMOV+bPE+73j+JlQMIr7YLUjOXGjkfWoNDP/LzH7VB8NvVnQH2MQZqyV3homCtdS+mYdnwJK8Y4CRRQ51tyQHPcbJN0QZnOQrIqhUbtFknalDcXQWEg/WuT12fcP2JaJZKtFHXzSQa7iXxEbeF907sn87yN+8DhfhjYY+lMq7spW6jlB28AnCjpMUCO/frngHnuGFE+7Cb4e+IwLBm5YAYf4u9qrCD+4ILkYjUsxxm9Pyk9GdFMOdRgwWNdvCBYITuoREkZMj+Ro1/5pjpL0qSGZtHmNqaMib85OPfk7unqv60CUkzS7lKlPZYCxtzSmLl/c6TN6a7KOdJr9MAUXPAfhl74sqpjAv3BlCWlopSIWsVnQv+ChBq6iQoT8IzJgXz; bm_so=30061D21AA5FD42BEE53FDE309955FD2A0E58C1417BD86B24266317B9D3711D7~YAAQz0vSF5eFa9qbAQAAFV5B9wZUanZ7Ga9pmPFxx48riKF34EE9vsJJz3JV6Y92uDopfkKPP4mevAUKouk8jJDVksz71wHhfC/ILjfnFzgI5pvcy3Q0OxtURCYdGmsLtB0VutpYmuIY2b5DIDWKIkU8b4UYrK7eGtUt3SDV2APsk2576SNKakZa7RC2iV4Wur9Zicno790dkaOGh7NuWZUeH65B6fAxz/oWt3AjnAdT9TeKKkS66PJpVs57iarnHav3Wsm1kzqENaRWGkKmMeKZpdskKZL4gTjpTM4BCMxqACPnPSjdZwTGPXYG93mgVTEBubpRI1BiE72lVMOs6ZqiP0wWK/GIsgmHC+lXKDSoXdub0/6ZtKwpvUDqUAA0zOnZBrHPSZ5iKXZHzNkRonPYe082mqw5Ugevm05ZM9BuAKWoRg0IPGBgVCU02VtTu1JSdsep7U1XxQfZ; hmid=1408110B-B1EE-49D3-897D-D1B2D08F29DD; bm_lso=30061D21AA5FD42BEE53FDE309955FD2A0E58C1417BD86B24266317B9D3711D7~YAAQz0vSF5eFa9qbAQAAFV5B9wZUanZ7Ga9pmPFxx48riKF34EE9vsJJz3JV6Y92uDopfkKPP4mevAUKouk8jJDVksz71wHhfC/ILjfnFzgI5pvcy3Q0OxtURCYdGmsLtB0VutpYmuIY2b5DIDWKIkU8b4UYrK7eGtUt3SDV2APsk2576SNKakZa7RC2iV4Wur9Zicno790dkaOGh7NuWZUeH65B6fAxz/oWt3AjnAdT9TeKKkS66PJpVs57iarnHav3Wsm1kzqENaRWGkKmMeKZpdskKZL4gTjpTM4BCMxqACPnPSjdZwTGPXYG93mgVTEBubpRI1BiE72lVMOs6ZqiP0wWK/GIsgmHC+lXKDSoXdub0/6ZtKwpvUDqUAA0zOnZBrHPSZ5iKXZHzNkRonPYe082mqw5Ugevm05ZM9BuAKWoRg0IPGBgVCU02VtTu1JSdsep7U1XxQfZ~1769379817879; utag_main__sn=16; RT="z=1&dm=hm.com&si=df09a1f5-4dcc-428f-baad-88310059d0f5&ss=mku8kv7g&sl=e&tt=kcr&bcn=%2F%2F684d0d47.akstat.io%2F&ld=2h9eh"; hmgroup_consent=datestamp=2026-01-22T10:10:17.890Z&url=https://www2.hm.com/en_in/index.html&consentId=800d4e50-c2a4-41b5-9626-45368e5a16fb&groups=C0001:1,C0002:1,C0003:1,C0004:1; OptanonConsent=datestamp=2026-01-22T10:10:17.890Z&url=https://www2.hm.com/en_in/index.html&consentId=13746239-a11d-423c-ba2f-651050f9e093&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; _cs_ex=1756732829; _cs_c=0; _scid=Ep-7EpVUWUu7vkvb3afy5fikd5WHsJV9; _gcl_au=1.1.1921001708.1769076620; _ga_Z1370GPB5L=GS2.2.s1769375657$o17$g1$t1769379817$j60$l0$h0; _ga=GA1.2.1367724838.1769076620; _pin_unauth=dWlkPU1XVmtORGs0WXpJdE5UTXlNQzAwTjJOaUxXSmpaalF0TkRNMFpETmxNR1ZpTWpBeA; _tt_enable_cookie=1; _ttp=01KFJJY010X1JS41K0ST8CVFRT_.tt.1; ttcsid_C4QSSN7M5GFN4SM6UID0=1769375665116::rfnLHjaTVdIQjbNudmzZ.17.1769379656209.1; ttcsid=1769375665116::cYYwfj-PcTcnXflaLW-m.17.1769379656209.0; _fbp=fb.1.1769076621433.23438204642428262; _sctr=1%7C1769020200000; agCookie=731ad8e3-db51-4dc0-959a-09411a00e7e8; _abck=6E45CCF7707BF3A8EE09135495486E80~0~YAAQz0vSF1mBa9qbAQAAE7I+9w/nIKsb4+04vk8zVm+BmlwbflARS/Tx4BCIdYWznTfHdTrm3Qg5fuDq3F+/ZLFXEdJYTthMxSQ0eJdWCl8D3cQKANaUIHQV0N2fSqdFcrGwNV37Yxu80Ad0DzH3i4s0G585+LDcfmoku39Aj9CJKSn2iJ8V8oRCbPior9h2DaC2c/kFabSkuNA3YFBhmaLHpCd2yJOsAM+oy+nnKWc25idQpD8v9HK1pELbRcQr50rvkFIM/v7C+EKZLgeQFrcCa4CgbhkNXEexkLcRo9n1BxIsFq1BI0z1WvS5NhbMiroC+nSsk6MIzw9imEMaOvAOFJjWWp1z97qFdSgxo4INGJ6qxN4ygdZqVuE9HS0EJ4p7wgmgHj86gx03RZXksVZjOWrcKlhPviz+llQCOiBQ0iMIQqji9lhUG3QlkxKrUW5MbkVXeY3LhHcGkIHXFvi80in0SHiRjLNRJgMOQgJW2eaoII0q8qhxBHup/XBdRQ6rt52N0AZwbYh3xg1eWPJHMRMbz3aeTQ2ZMVnNlMtHOvAatjrPSekBLP02g681+ZKdgr7D2v8UxwDeVyJqQAcf6HE47zAqBYFSyMj0oZc+Lwgq2NN4nhYMS6LK52aZFtqHV0H2siM0zz02QTku8s1UpgPpPp6kfwWGqvoBvsvr4gZcVdIlW808/v4IdpUuHu2JO+slyZACmMoL3Xs=~-1~-1~1769381912~AAQAAAAF%2f%2f%2f%2f%2f6SMhIwjssxYcrPch3MeWUp3JrHk8eFhylCkWu%2fE7gPy3yA5NMZL9yKtNfXCl8T+o5003MwVRKvylhpx28JfbMkI%2fEqvFhEoqebqDhKJQ8dUeJx9isu%2fOyzU+FSmqubfPEsLLVjZ2DO2jym6pPge+c8Bt4yhnjQEK7uVLlInfA%3d%3d~-1; hm-india-cart=17209be6-cbb9-45f8-b42a-bcb6b4a9a3d2; akainst=APAC; akamref=; bm_sz=47CC91871AD28BB89F6106AA1B1C194E~YAAQz0vSF5mFa9qbAQAAFV5B9x4/zJYYTGhi2o8143W4sXX6rcQTPINDbAiAGwckDAB7PYzSDuGa5ecnyb1c/BG2ejeJgD7OpJJoRFGj7L4YBd8VG3FtzlKVhcsANp1aNpodPuWt90wra1n+VT2O1y5gaC3gXaRqEPs6kTdtB1S5aQD5tQLeSxZI11hFndAOYPxgvBoITa1xztaidK3Ky2U61AWRqtTMEHD7nC0NVdFlkgIyJSEGfgJkfS4TS1Xh7EIrhJvqUWZx8hf9dbPXFY1LlqvsMRG8ICn07/WqlYvuaVRTDCLni1SVIYYWhDRJ388JXHOR1KcgjT0W3mXkHFquWHOznMZx21m2eniuiO6pOZA+02c21mvKAMBNOqOKvaKAbArkbvkwusQOeaV3mq/eVUz0E68PXcQTMp9INk6zKIsfhLfLw4FQzcMmsJzgUZr74pm3577WU4HqErPzpUyl2eTwLyF9+4MZ5eiD2YHOwpBROSgFEKADmHFQY6ybkChqP85LHb3xHjbRtA==~4534326~4470841; akavpau_www2_en_in=1769380116~id=8a386eb70a085cfb44ccb4f2649c99c0; bm_sv=E3970D5A034B67ECDC446169B233945F~YAAQz0vSF6eFa9qbAQAAo2RB9x6COsxPJUDYO+uXe7EjHCn6wFGf2y3031RbbHW4xqqj0zTY6DOuz/t+Lu8iPhf2MqDUCNWuyElQWZDcQ1ygONUFZaeMY7damKosUkFsPKKD2qxuy8pPDFsXt4bYl3DAfo3xS1rBpjZuBb+MEqdHdbmyWDpFGC1R7i45uAx50z7MQQMMPNhYl+5A3VRS3aLWqx2A0rdoidE8F76MfgtYZL0ELmD/UzLDbSYm~1; INGRESSCOOKIE=1769371117.365.394.941193|7bbf721d92a09b08c42eb8596390c8cc; JSESSIONID=6A15F52D74E39C121F2D101AB135614C6E76FD02B7D79BB99314781D9E62D6C51C0833806EBAC964BA146935A2929E2F5F9D32DF3DD69C9A52E64854D5C70092.hybris-ecm-web-849ffc645b-qmgnl; userCookie=##eyJjYXJ0Q291bnQiOjB9##; utag_main__se=113%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__st=1769381617856%3Bexp-session; utag_main_ses_id=1769375655189%3Bexp-session; utag_main__pn=15%3Bexp-session; dep_sid=s_6543228224842531.1769375655191; dep_exp=Sun, 25 Jan 2026 22:53:37 GMT; ak_bmsc=69714F89FAAC8E0EC59E9F2A5BA8CC01~000000000000000000000000000000~YAAQz0vSF16Ba9qbAQAAfLg+9x6Pv/E6Ya2FzVljUCGvalOmdtpz3Glr769/X0cK2hhDq2SpRpjKGCtWt7gZ4eW8s9arsfSrUDcRQPlTD51NuUxVAnaQHssa3FQf7bOISnXjmJC+ehHepZ6z0G6Qd/+1rH/Vyqmveb4HPs8VBZvxRx7AHsctQ3dkhaEb4qMuaAutLouYK7lovIHxkmuXq0jbuwZImDMDR3DN4DTBqglY7+bYtJohjbsbn9IqWJji1QvIIFzGiV61l6k6hgAjokKPSkONlrJQ4WtRCNMLS9rMABvnTevwdm82Y/9waI83ONkwWjGiUUkfQ8Hu2spiesAlzFwVGxARAgf7I97K7d8U1pOVCOduGbYIgb/GCMnFxOgDdvebc3SJqARM0s5cXtarDModO4hpGIBybZ8Sd2sq+c7lChPyEvfMiKqzdGm8FEbJnP4xU74x2iFlL4h10r/kqla+IP+cr+lbk/xgY9FsNu3BhemSPJEJ3flQ6NM=; AKA_A2=A; bm_ss=ab8e18ef4e; bm_mi=A81C43387F30A5DFF356BFE22550D24F~YAAQz0vSFzuBa9qbAQAAeqU+9x6PzTQxTQimFgfYN/xLeCbmg2GrTfR/APrg6uWsyp8C84xskK2YvXY4PHYWdbvJIFJZvHr4TEuSUcEKqLvNk7FJJobusxUaAW05UwTJQDdNk2xphqNuw09moAWeDaRBKPYkqNMue3uIzEyF8PcMVEMGaEY/Sg6N/i9VmCGZ6C4wlFXwYXUnRRFie5j4StYo5yAicPuu+SxbrtMJ3I9y1BfbUc2zuoHkMovn3COxwi35ptZ9kdeWG8oZ3dtsKLOCNfFi+2dSSVwrWLj9M3Yw9Wkye/h3h/e9+Q4AjpB24ZhagVHnYjQIgKC1~1; bm_sc=4~1~34978766~YAAQz0vSF1WBa9qbAQAAg7A+9wZU2gfEfzmiS3VHFLwxIdBrAuqn65asPyUzx6OO+PLfIKeSLJ8xl3+hWYdt9tZLPyaK3zXV+jxC3acwyM8YVEUI4UENXwTU+5lNZFv99C4ZxzGP8dG1Gtu8UBNtxHS6kDF7TsO+HBORT3HIZxAtMJbim8SmQ4dv151nmoiBrTBMLCU9oSv+NaZc1VPijx7aD2UyXId0X2Rj7K9WGAiaVbX6lfAsdVcF1jgBKbr/WMtQgUDi909G+nmudhQvco1z+5dpzGZuXi5YNOnkBuwoE1DOXgKYjzWqVrlZ+jlUfqnjTyDngVycYmjA8zp2FDJVlCQ49gsnTGDKJn09uQa+PmD9Dr1Dr3Nb+sF3GmocEQYrOE++Nl5DdDxh/U1co+D/43shakj/3B8eEe4RNd9Javf3HuFvb0cp7bFFYUs3BqVC4A1v+rPL2x8BTMtSFORP/myzgcUUQcdpLauJsCLYDpGV5+IlyVzHus2qC00oip8EqqG+xgHpi0gWb0ZcWCATc2qqC2V/TlqWW62WfctH237zWZZjujpnQtqIcH3turfBmzDjJcEp39QweveoWVdpiv9YZSIJW8Wrw8KlDB+dJmhIEirrWezapWuBjjFKD43w5z2SsIjvzr63Pm1NvYc3rSQL3GoHs4NaBJf87Rk=; dep_testdata=normal; _uetsid=acadd9d0f94b11f0957f8fa9fe3cd629; _uetvid=8e971c40f77a11f0b6d8ad4d3a7ff761; _scid_r=Mx-7EpVUWUu7vkvb3afy5fikd5WHsJV9mJ8Psw"""
}

PARAMS = {
    "pageSource": "PLP",
    "page": 1,
    "sort": "RELEVANCE",
    "pageId": "/men/shop-by-product/view-all",
    "page-size": "36",
    "categoryId": "men_viewall",
    "filters": "sale:false||oldSale:false",
    "touchPoint": "DESKTOP",
    "skipStockCheck": "false"
}

CLIENTS = [
    "chrome_120",
    "chrome 117",
    "firefox_117"
    "firefox_120",
]


def save_to_csv(data):

    if not data:
        print("no data to save")
        return
    print("saving data to csv....")
    time.sleep(2)
    headers = data[0].keys()

    with open("data.csv","w",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} records successfully")



def save_to_mongo(data):     
    try:
        connecion = "mongodb://localhost:27017"
        client = MongoClient(connecion)
        db = client.get_database("training_db")
        collection = db.get_collection("H&M")
        collection.insert_many(data)
    except Exception as e:
            print(f"mongo error: {e}")
    print("suscessfully entered data into mongodb")




# def parser(url):
#     session = tls_client.Session(client_identifier="chrome_117")
#     product_response = session.get(url,headers=HEADER)
#     print(product_response.status_code)
#     html = product_response.text
#     print(html)
#     selector = pq.Selector(text=html)

#     breadcrumbs_fetched = selector.xpath('//ol[@class="b43307 ea1998"]//text()').getall()
#     prod_url = product_response.url
#     breadcrumbs = "".join(breadcrumbs_fetched)
#     Title = selector.xpath('//h1[@class="b9e19c c779b4 b44f77"]//text()').get()


#     selling_price = ""
#     regular_price = ""
#     selling_price_fetched = selector.xpath('//span[@data-testid="red-price"]//text()').get()
#     if selling_price_fetched:
#         regular_price_fetched = selector.xpath('//span[@data-testid="line-through-white-price"]//text()').get()
#         regular_price = float(re.search(r"\d[\d,]*\.?\d*", regular_price_fetched).group().replace(",", ""))

#         selling_price = float(re.search(r"\d[\d,]*\.?\d*", selling_price_fetched).group().replace(",", ""))
#     else:
#         regular_price_fetched = selector.xpath('//span[@data-testid="white-price"]//text()').get()

#         regular_price = float(re.search(r"\d[\d,]*\.?\d*", regular_price_fetched).group().replace(",", ""))

#         selling_price = regular_price

#     Description = "" 
#     Description_fetched = selector.xpath('//p[@class="fdb3e1 cfeb83 b493f8"]//text()').get()
#     if Description_fetched:
#         Description = Description_fetched
    


#     Net_quantity = ""
#     Net_quantity_fetched = selector.xpath('//dd[@data-testid="description-netQuantityAccordions"]/text()').get()
#     if Net_quantity_fetched:
#         Net_quantity = Net_quantity_fetched
    
#     Fit = ""

#     fit_fetched = selector.xpath('//dd[@data-testid="description-fits"]/text()').get()
#     if fit_fetched:
#         Fit = fit_fetched

#     country_of_origin_fetched = selector.xpath('//dd[@data-testid="description-countryOfProduction"]//text()').get()
#     if country_of_origin_fetched:
#         Country_of_origin = country_of_origin_fetched
#     else:
#         Country_of_origin = ""    
    

#     diamentions_fetched = selector.xpath('//dd[@class="fdb3e1 cfeb83 f1bad1 acddb1"]//text()').getall()
#     if diamentions_fetched:
#         converted_string = " ".join(diamentions_fetched)
#         pattern = re.findall(r'Width:\s*([\d\.]+\s*(?:cm|m))\s*,\s*Length:\s*([\d\.]+\s*(?:cm|m))',converted_string)

#         Diamentions = []

#         for width, length in pattern:
#             Diamentions.append({
#                 "width": width,
#                 "length": length
#             })
#     else:
#         Diamentions = ""
    






    
#     fabric_composition_fetched = selector.xpath('//li[@class="b819ff"]//text()').getall()
#     if fabric_composition_fetched:
#         Fabric_composition = {}
#         current = None
#         for i in fabric_composition_fetched:
#             if i.endswith(":"):
#                 current = i.replace(":","")
#                 Fabric_composition[current] = {}
#                 continue

#             parts = re.findall(r"([A-Za-z ]+)\s+(\d+%)", i)
#             parsed = {name.strip(): percent for name, percent in parts}

#             if current is None:
#                 Fabric_composition.update(parsed)
#             else:
#                 Fabric_composition[current].update(parsed)
#     else:
#         Fabric_composition = ""

    

#     care_instructions_fetched = selector.xpath('//ul[@class="e00dc3"]//text()').getall()

#     if care_instructions_fetched:
#         Care_instructions = ",".join(care_instructions_fetched)
#     else:
#         Care_instructions = ""


#     model_fit_fetched = selector.xpath('//dd[@data-testid="description-modelHeightGarmentSize"]//text()').get()

#     if model_fit_fetched:
#         Model_fit = model_fit_fetched
#     else:
#         Model_fit = ""


        

    


#     return {
#         "Url": prod_url, 
#         "Breadcrumbs": breadcrumbs,
#         "Brand": "H&M",
#         "title": Title,
#         "Regular_price": regular_price,
#         "Selling_price": selling_price,
#         "SKU": "N/A",
#         "Description": Description,
#         "Diamentions" : Diamentions,
#         "Net_Quantity": Net_quantity,
#         "Fit": Fit,
#         "Care_instructions": Care_instructions,
#         "Fabric_composition": Fabric_composition,
#         "Model_fit": Model_fit,
#         "Country_of_origin" : Country_of_origin,



#     }
# print(parser('https://www2.hm.com/en_in/productpage.1096385010.html'))









    
    




# def crawl(url):
    
#     list_of_pdp_urls = []
#     #while True:
#     session = tls_client.Session(client_identifier="chrome120")
#     response = session.get(url,headers=HEADER,params=PARAMS)
#     print(response.status_code)
#     data = response.json()
#     products = data["plpList"]["productList"]
#     if products:
#         print(f"[INFO] Fetching product urls from {PARAMS['page']} ")
#         for i in products:
#             print(i["url"],end="")
#             list_of_pdp_urls.append(i["url"])
#         print("INFO Fetched urls")
#         #PARAMS["page"] += 1


#     print(len(list_of_pdp_urls))
#     print(list_of_pdp_urls)


# crawl(URL)

