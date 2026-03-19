import hrequests
from parsel import Selector


headers = {
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.9',
'Accept-Encoding': 'gzip, deflate, br, zstd',
'Referer': 'https://www.carrefour.be/nl/dranken/softdrinks',
'Connection': 'keep-alive',
# 'Cookie': '__cf_bm=tYAqHp102GvRP9JzjFDmeA1MQuaTt.xyoPFA4aAejzU-1773894879.485494-1.0.1.1-hA4s_tLW_NWQWoGPJYMFX2Aovgkj7tMzLMVItMIfk0phocMLTEDf96GYyd_._VQuQMxblpzh4L5vbUXsTN90tK.z3s6DvgqKEBgCus76ee_pZDEfTXT_Vyk_nJlAewcj; cf_clearance=cDNOV0264Vy9nRphnoMAp7inC0puikHWEjuW_GmP.aY-1773894879-1.2.1.1-KbGs4DTtpAonFTYtrpS.rDT4onW0Qs4EJ4bh1v52aKbW_pOSjLJtZ3gdQtb2tdTOdwG.1jRK4PXF_8R0VmgSMi7byhKHiPF76UaUv72ItDc_n_1XlnNd1oHyTHLBzVGsy.J7JjBLBQPzzyUM5DquWvsDD4B.OKw7enRjErdbMbL.tS6FzGS4gfRU.BJ0C5j3yJJnEnUoNj2.QHARMd9e4ZQmxkX1A854g08Dk73ZT1tApTyAofkyaMJx9lSmrg_w; usid_carrefour-be=d1d7f75d-22c7-418d-8019-145f0dfa00ad; dw_store=0615; sid=EEWExfpafqIrrfORZKEs2ZL3vjQuKHXvM1Y; cc-nx-g_carrefour-be=l-LbumT6rWgm2Z2UeKe3ZeDhqXRqeRuA1h78HDsNJN8; dwsid=n_nwUpykLFh7m7_tgc2PKB1LyqNI1icVY2Aa2AQHZ0ZRsa0LGObV-F1qME4OB8oR31hBbDCFOzRdfSTWdPCwog==; dwanonymous_3e7c08d0a46f12ebb778e9dc0c5c9f8e=abq9k4ohUs0PxYRv28ZzCVJgKH; __cq_dnt=0; cc-at_carrefour-be_2=Nob3BwZXItZ2lmdC1jZXJ0aWZpY2F0ZXMgY193aXNobGlzdF9ydyBjX2N1c3RvbWVyQ2FydF9ydyBzZmNjLnNob3BwZXItcHJvZHVjdC1zZWFyY2ggc2ZjYy50c19leHRfb25fYmVoYWxmX29mIHNmY2Muc2hvcHBlci1zZW8gY19jb250ZW50X3IgY19wb3B1bGFyU2VhcmNoVGVybXNfciIsInN1YiI6ImNjLXNsYXM6OmJrbnRfcHJkOjpzY2lkOjk5MjQ4MDY3LWYzOWQtNGI4OS04MDZhLWY0NGUxZWQwMzUxNzo6dXNpZDpkMWQ3Zjc1ZC0yMmM3LTQxOGQtODAxOS0xNDVmMGRmYTAwYWQiLCJjdHgiOiJzbGFzIiwiaXNzIjoic2xhcy9wcm9kL2JrbnRfcHJkIiwiaXN0IjoxLCJkbnQiOiIwIiwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JrbnRfcHJkIiwibmJmIjoxNzczODk0MTE2LCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDphYnE5azRvaFVzMFB4WVJ2MjhaekNWSmdLSDo6c2VzYjpzZXNzaW9uX2JyaWRnZTo6Y2hpZDpjYXJyZWZvdXItYmUiLCJleHAiOjE3NzM4OTU5NDYsImlhdCI6MTc3Mzg5NDE0NiwianRpIjoiQzJDMTA3ODY2ODA3MDAtMTI5NzYzMTAxOTE2MjAzNjAxODE2NTcyMDc2In0.kazerQvOUsLyXIY0Ktgj5xilfhzF8LA3nKE3cqrsIzgnqL5iEiysFSM2r22Qm7gaXSICClmlvTZU4pBs8VziaQ; dw_dnt=0; cc-at_carrefour-be=eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmtudF9wcmQiLCJraWQiOiIxZWQwMWJmNC0zNGQ2LTQxOTAtYTdkNC0zODUzMmEyY2ViZmIiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gY19hdXRoX3Igc2ZjYy5zaG9wcGVyLWV4cGVyaWVuY2Ugc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgY19ib251cy1jYXJkX3Igc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNlc3Npb25fYnJpZGdlIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzLnJ3IGNfY3VzdG9tZXJCYXNrZXRfcncgY19hZGRyZXNzX3IgY19jdXN0b21lck9yZGVyc19yIGNfY2JjX3J3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzIHNmY2Muc2hvcHBlci1jYXRlZ29yaWVzIHNmY2Muc2hvcHBlci1teWFjY291bnQgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RzIHNmY2Muc2hvcHBlci1teWFjY291bnQucncgc2ZjYy5zaG9wcGVyLXN0b3JlcyBjX2NvbmZpZ19yIHNmY2Muc2hvcHBlci1iYXNrZXRzLW9yZGVycyBzZmNjLnNob3BwZXItY3VzdG9tZXJzLnJlZ2lzdGVyIHNmY2Muc2hvcHBlci1teWFjY291bnQuYWRkcmVzc2VzLnJ3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzLnJ3IHNmY2Muc2hvcHBlci1iYXNrZXRzLW9yZGVycy5ydyBzZmNjLn; cc-sg_carrefour-be=1; OptanonCleared=1; carrefour_be_lang=default; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+19+2026+10%3A10%3A21+GMT%2B0530+(India+Standard+Time)&version=202407.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=91794d8b-5573-4c23-8bc2-b2fc636e8f8a&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0054%3A1%2CC0022%3A1%2CC0304%3A1%2CC0007%3A1%2CC0279%3A1%2CC0246%3A1%2CC0052%3A1%2CC0038%3A1%2CC0222%3A1%2CC0023%3A1%2CC0032%3A1%2CC0057%3A1%2CC0041%3A1%2CC0122%3A1%2CC0079%3A1%2CC0004%3A1%2CC0223%3A1%2CC0096%3A1%2CC0051%3A1&intType=1&geolocation=%3B&AwaitingReconsent=false; citrusConsent=true; OptanonAlertBoxClosed=2026-03-19T04:22:43.160Z; _cs_mk_ga=0.9048326873513242_1773894163189; _gcl_au=1.1.1990971874.1773894163; _ga_HZ1NJYS59D=GS2.1.s1773894163$o1$g1$t1773895221$j59$l0$h100768711; _ga=GA1.1.1523763888.1773894164; _pin_unauth=dWlkPVptVmtNR014TW1JdFlUUTJOaTAwTVRkaUxXSTJZVFV0WkRZME1UaGpPVFEyWXpnMg; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.carrefour.be%252Fnl; ABTasty=uid=s23kb48yx7ykxezj&fst=1773894165359&pst=-1&cst=1773894165359&ns=1&pvt=22&pvis=22&th=; _fbp=fb.1.1773894165590.565897341691931932; fs_lua=1.1773895222030; fs_uid=#o-A8T6-eu1#39ba4583-7cde-4d72-a176-3376e1d8dd7a:89d91fdf-3335-4304-b86c-0c93f336ece4:1773894165260::16#/1805430196; tfpsi=40fa3533-bde8-45c7-9cc8-a77eff7c2d44; dwac_49875165c7052266a00c48df9a=EEWExfpafqIrrfORZKEs2ZL3vjQuKHXvM1Y%3D|dw-only|||EUR|false|Europe%2FBrussels|true; cqcid=abq9k4ohUs0PxYRv28ZzCVJgKH; cquid=||; citrusAdSessionId=5f4071141ddc2eed71f18773be; __cq_uuid=abq9k4ohUs0PxYRv28ZzCVJgKH; __cq_seg=0~0.24!1~-0.24!2~-0.18!3~0.06!4~0.71!5~0.38!6~-0.26!7~0.22!8~0.21!9~0.20; __cq_bc=%7B%22bknt-carrefour-be%22%3A%5B%7B%22id%22%3A%2201505667%22%7D%2C%7B%22id%22%3A%2206839603%22%7D%5D%7D',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Priority': 'u=0, i', 
'TE': 'trailers',
}
######### C R A W L E R ################
response = hrequests.get('https://www.carrefour.be/nl/orange-lemonade-6-x-500-ml/01505667.html',headers=headers,)
print(response.status_code)
sel = Selector(text=response.text)
products = sel.xpath('//div[@class="gtm-event"]').extract()

link = './/div[@class="gtm-event"]//div[@class="name-wrapper js-product-tile-gtm"]//@href'




##############PARSER######################


response = hrequests.get('https://www.carrefour.be/nl/orange-lemonade-6-x-500-ml/01505667.html',headers=headers,)
print(response.status_code)
sel = Selector(text=response.text)
product_name = sel.xpath('//h1[@class="product-name"]/text()').extract_first()
brand = sel.xpath('//div[@class="grouping-brand-name-badge"]/div[@class="brand-wrapper"]/div/text()').extract_first()
breadcrumbs = sel.xpath('//div[@class="desktop-breadcrumb"]/div[contains(@class,"breadcrumb__item")]//text()').extract()
regular_price = sel.xpath('//div[@class="pdp-tile col-12 col-xl-5 "]//div[@class="price"]//text()').extract()
print(product_name)
print(brand)
print(breadcrumbs)
print(regular_price)

