import logging
from pymongo import MongoClient

DOMAIN = "https://www.carrefour.be"

COOKIES = {
    'cf_clearance': """xEGpml4sKSwtLaS.sQh18IlkMWJ6zDb_DmbJd0lRkp8-1774380852-1.2.1.1-7.OdqwWOyeQvoQSE4il5kN3nOmm.vMd.PHGF3Gnyw2hVvXX3HXFozdN2.omF.u2.zQLQvj8r8oIkFDx.fIkKYgRq44nhJ7jH.GShx.fR6PIiudZo8S3hxupcNgApcUofrXHb0.JxBhTxJZ.3_eFCoD1AfUePo9RMXzhNtahaRteR144AcrLmWKzGNnYT6RcqY_YqsP43a3DDsAP5hDTXn3RE6b4YSynY2j5ZZNVUW5N.NvUzlZ3Fwya9FvZOjGXL"""}
    # HEADERS = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'referer': 'https://www.carrefour.be/nl/dranken/softdrinks?__cf_chl_tk=rqstSICh0mS.ZQU4W93q2bAqTplA6wYv1nBUItWLyCQ-1774333024-1.0.1.1-w7wkhSqRb3cjQU1F9_5f80izr2lmj.vNuxTglFlWwZM',
#     'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
#     'sec-ch-ua-arch': '"x86"',
#     'sec-ch-ua-bitness': '"64"',
#     'sec-ch-ua-full-version': '"145.0.7632.159"',
#     'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.159", "Chromium";v="145.0.7632.159"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Linux"',
#     'sec-ch-ua-platform-version': '""',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
#     # 'cookie': 'usid_carrefour-be=8c9443b3-f431-4ab5-91c2-64ed2672c2b1; dw_store=0615; cc-nx-g_carrefour-be=n-xcu7j5-QMM1SFuZv3V00eWvstcx1r6gZ6UsgISPhI; dwanonymous_3e7c08d0a46f12ebb778e9dc0c5c9f8e=abNxiJTB9jkI5jjw8Krkmg1FGE; carrefour_be_lang=default; OptanonCleared=1; OptanonAlertBoxClosed=2026-03-19T06:05:06.098Z; citrusConsent=true; _gcl_au=1.1.1511655160.1773900306; _ga=GA1.1.1695396121.1773900307; _fbp=fb.1.1773900308284.272689432301209018; _pin_unauth=dWlkPVpHTmhNak0xWVdJdFl6SXhNaTAwT1RreUxUZ3labUl0WWpFNE1EZGxPV00wWmpNNA; dwsecuretoken_3e7c08d0a46f12ebb778e9dc0c5c9f8e=""; dwsid=IacBYIcEheSbjdWPuBjeLBnxMyJiSZtcj22_vvEl1mRQNgh4HCV6H1JwHbCz4SN6ctVaSNMbcNyzZU6PcDMfRQ==; __cq_dnt=0; cc-at_carrefour-be_2=Nob3BwZXItZ2lmdC1jZXJ0aWZpY2F0ZXMgY193aXNobGlzdF9ydyBjX2N1c3RvbWVyQ2FydF9ydyBzZmNjLnNob3BwZXItcHJvZHVjdC1zZWFyY2ggc2ZjYy50c19leHRfb25fYmVoYWxmX29mIHNmY2Muc2hvcHBlci1zZW8gY19jb250ZW50X3IgY19wb3B1bGFyU2VhcmNoVGVybXNfciIsInN1YiI6ImNjLXNsYXM6OmJrbnRfcHJkOjpzY2lkOjk5MjQ4MDY3LWYzOWQtNGI4OS04MDZhLWY0NGUxZWQwMzUxNzo6dXNpZDo4Yzk0NDNiMy1mNDMxLTRhYjUtOTFjMi02NGVkMjY3MmMyYjEiLCJjdHgiOiJzbGFzIiwiaXNzIjoic2xhcy9wcm9kL2JrbnRfcHJkIiwiaXN0IjoxLCJkbnQiOiIwIiwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JrbnRfcHJkIiwibmJmIjoxNzc0MzMzMDAxLCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDphYk54aUpUQjlqa0k1amp3OEtya21nMUZHRTo6c2VzYjpzZXNzaW9uX2JyaWRnZTo6Y2hpZDpjYXJyZWZvdXItYmUiLCJleHAiOjE3NzQzMzQ4MzEsImlhdCI6MTc3NDMzMzAzMSwianRpIjoiQzJDMTA3ODY2ODA3MDAtMTI5NzYzMTAxOTE2NjQyNDg3MjM4NTc2NjA4In0.Op5wf8HmIMdKbjFbPjGJ1UcfsilpjBkqfTki6pHkucrA7oThCvAzQNmEvlNjFEVH9UmRoaUnHaG4wSw741OgaA; dw_dnt=0; cc-at_carrefour-be=eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmtudF9wcmQiLCJraWQiOiIxZWQwMWJmNC0zNGQ2LTQxOTAtYTdkNC0zODUzMmEyY2ViZmIiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gY19hdXRoX3Igc2ZjYy5zaG9wcGVyLWV4cGVyaWVuY2Ugc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgY19ib251cy1jYXJkX3Igc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNlc3Npb25fYnJpZGdlIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzLnJ3IGNfY3VzdG9tZXJCYXNrZXRfcncgY19hZGRyZXNzX3IgY19jdXN0b21lck9yZGVyc19yIGNfY2JjX3J3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzIHNmY2Muc2hvcHBlci1jYXRlZ29yaWVzIHNmY2Muc2hvcHBlci1teWFjY291bnQgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RzIHNmY2Muc2hvcHBlci1teWFjY291bnQucncgc2ZjYy5zaG9wcGVyLXN0b3JlcyBjX2NvbmZpZ19yIHNmY2Muc2hvcHBlci1iYXNrZXRzLW9yZGVycyBzZmNjLnNob3BwZXItY3VzdG9tZXJzLnJlZ2lzdGVyIHNmY2Muc2hvcHBlci1teWFjY291bnQuYWRkcmVzc2VzLnJ3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzLnJ3IHNmY2Muc2hvcHBlci1iYXNrZXRzLW9yZGVycy5ydyBzZmNjLn; cc-sg_carrefour-be=1; sid=ivVAC-jx0Xkn4psLOyxZ8bKjckkNvM_BMwI; dwac_49875165c7052266a00c48df9a=ivVAC-jx0Xkn4psLOyxZ8bKjckkNvM_BMwI%3D|dw-only|||EUR|false|Europe%2FBrussels|true; __cq_uuid=19ac3c90-2749-11f1-8394-ffc1b6a2d4dd; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; _cs_mk_ga=0.2251312456088973_1774333039319; cqcid=abNxiJTB9jkI5jjw8Krkmg1FGE; cquid=||; citrusAdSessionId=aecd49759fc13ae04246cc2665; cf_clearance=ewoW9FAgOt5ZwbT1sxTe0onbpNn1VyXzXVn31QXk4ww-1774333042-1.2.1.1-bYQN2NFfp.rO.E5OR7QF3F9OzXlgHP0XSjPJ8j3b9B2pB2hxwq9IQMWOLjQk0Ow5a2.gayCJ.xqpS3Dj63snggSdwNmxDm1L5J0LSfP_4d35N7PCUCJBoFag_F8V923sTHjJ2Abg0h03krpIov7RNQcMwvCMl.JeSHF8ZbJPMMSeBmL06HTglL61iuRwIvJGYDvUmrK7dELEEuJ1f0nXVQyYYeqCFWQQ_fuMmlP0BeCRdWiorlkviujiOJcx.w9R; __cf_bm=ap9BiX8cNUNvT7ERBNo_SCA7kR1KLYRugQ_CU26n3QQ-1774333042.7247765-1.0.1.1-poPkT6lo0M6I5fK1176gQjiDPEukmcAA6ol28j2kFqO7H.jVn3B_x96YDb.zbl2SUCuaq6g5JdcrfV8Y5oWA.w9vKkSM.ZRcziuXoB8EzRbqjOsp7MJGfEZQSzIkEzQ4; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.carrefour.be%252Fnl%252Fdranken%252Fsoftdrinks; ABTasty=uid=f06jqb14ggyv6zvx&fst=1773900308652&pst=1773900308652&cst=1774333043639&ns=2&pvt=2&pvis=1&th=; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Mar+24+2026+11%3A47%3A24+GMT%2B0530+(India+Standard+Time)&version=202407.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=84b48415-8f53-4411-aff7-3f8eed67fc83&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0054%3A1%2CC0022%3A1%2CC0304%3A1%2CC0007%3A1%2CC0279%3A1%2CC0246%3A1%2CC0052%3A1%2CC0038%3A1%2CC0222%3A1%2CC0023%3A1%2CC0032%3A1%2CC0057%3A1%2CC0041%3A1%2CC0122%3A1%2CC0079%3A1%2CC0004%3A1%2CC0223%3A1%2CC0096%3A1%2CC0051%3A1&intType=1&geolocation=%3B&AwaitingReconsent=false; fs_lua=1.1774333044910; fs_uid=#o-A8T6-eu1#70f39b87-e853-425a-8fbf-436fe33081f9:0d22abf4-a495-4ea7-9e28-404695bb6873:1774333044910::1#/1805436311; tfpsi=406a9efa-6bc3-49a1-8488-014590c1d91b; _ga_HZ1NJYS59D=GS2.1.s1774333039$o2$g1$t1774333046$j53$l0$h1438377051',
# }
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.carrefour.be/nl/dranken/softdrinks?pmin=0%2C01&start=0&sz=36&p=1',
    'Connection': 'keep-alive',
    # 'Cookie': 'cf_clearance=7wn.LnZ4abD_tMQ9Liiba2zzGSF581Ex3jOAkbHYdcw-1773916570-1.2.1.1-6V4M2xfAJuCoruXSehY_j2alsuH_GLrKpHrSfH8XK5YenuDLmmapSE2yGvFOPF6S20f1KOS505MyTI65xa.m.hs74BSoSohX5cnu21IxpWEvCRS3n2z_1BPzSN61fuyDrQ50boEmXF2NzgPlkELLRtMBigJUHoEZRfYBI09Bf2PnUcXsYtbhgokuPT6oSFKquZTvoLq.ctr1b4XSnvHpKr_NsgfV1IJJ7pM1MipU6G1A5qm4HG1uTfOa3t6H6K89; usid_carrefour-be=d1d7f75d-22c7-418d-8019-145f0dfa00ad; dw_store=0615; cc-nx-g_carrefour-be=l-LbumT6rWgm2Z2UeKe3ZeDhqXRqeRuA1h78HDsNJN8; dwanonymous_3e7c08d0a46f12ebb778e9dc0c5c9f8e=abq9k4ohUs0PxYRv28ZzCVJgKH; OptanonCleared=1; carrefour_be_lang=default; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+19+2026+16%3A06%3A11+GMT%2B0530+(India+Standard+Time)&version=202407.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=91794d8b-5573-4c23-8bc2-b2fc636e8f8a&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0054%3A1%2CC0022%3A1%2CC0304%3A1%2CC0007%3A1%2CC0279%3A1%2CC0246%3A1%2CC0052%3A1%2CC0038%3A1%2CC0222%3A1%2CC0023%3A1%2CC0032%3A1%2CC0057%3A1%2CC0041%3A1%2CC0122%3A1%2CC0079%3A1%2CC0004%3A1%2CC0223%3A1%2CC0096%3A1%2CC0051%3A1&intType=1&geolocation=%3B&AwaitingReconsent=false; citrusConsent=true; OptanonAlertBoxClosed=2026-03-19T04:22:43.160Z; _gcl_au=1.1.1990971874.1773894163; _ga_HZ1NJYS59D=GS2.1.s1773914401$o5$g1$t1773916574$j56$l0$h972728842; _ga=GA1.1.1523763888.1773894164; _pin_unauth=dWlkPVptVmtNR014TW1JdFlUUTJOaTAwTVRkaUxXSTJZVFV0WkRZME1UaGpPVFEyWXpnMg; ABTasty=uid=s23kb48yx7ykxezj&fst=1773894165359&pst=1773909230508&cst=1773914405180&ns=6&pvt=82&pvis=6&th=; _fbp=fb.1.1773894165590.565897341691931932; fs_uid=#o-A8T6-eu1#39ba4583-7cde-4d72-a176-3376e1d8dd7a:46c997d9-480e-4b8a-ac69-9cc62b6f22ae:1773914403943::6#/1805430304; __cq_uuid=abq9k4ohUs0PxYRv28ZzCVJgKH; __cq_seg=0~-0.18!1~-0.29!2~-0.27!3~0.03!4~0.53!5~0.58!6~-0.37!7~0.13!8~0.18!9~-0.06!f0~3~1!n0~1; __cq_bc=%7B%22bknt-carrefour-be%22%3A%5B%7B%22id%22%3A%2206839603%22%7D%2C%7B%22id%22%3A%2206168827%22%7D%2C%7B%22id%22%3A%2206505924%22%7D%2C%7B%22id%22%3A%2207131903%22%7D%2C%7B%22id%22%3A%2207000301%22%7D%2C%7B%22id%22%3A%2206529443%22%7D%2C%7B%22id%22%3A%2206354914%22%7D%2C%7B%22id%22%3A%2206154863%22%7D%2C%7B%22id%22%3A%2207067414%22%7D%2C%7B%22id%22%3A%2201505667%22%7D%5D%7D; fs_lua=1.1773917297699; sid=uFZRAe_We2k61usYsjZlKWgOWmSUe3JwAWM; dwsid=MSNB9GS56GEvNsWGYyYR1-F7SpEfFOF4FIPL9KEddL06zgtQWba32Yw0wdzrQelSmV722wTGJtcIL5Z-iMCbBw==; __cq_dnt=0; dw_dnt=0; citrusAdSessionId=5f4071141ddc2eed71f18773be; __cf_bm=YsEBYq5JScqmqzOfMBW.W2_9lcAvbB1JVeC2NGPgyPk-1773916570.534813-1.0.1.1-_Zc3BDtCh1116Icf6rtE5Ff6FKA2wKlPdF3GHASrl1N99iEGz.hCRHZphvubXC3GJ3NIlFOv7WsI7SDZgtreW5foY4n9L15L4GwKF1gIOqvz5XW01AN8vedwmliUpRqh; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.carrefour.be%252Fnl%252Fdranken%252Fsoftdrinks%253Fp%253D1; tfpsi=c081b33e-e2eb-4234-a201-70f549b2b8b1; dwsecuretoken_3e7c08d0a46f12ebb778e9dc0c5c9f8e=""; cc-at_carrefour-be_2=Nob3BwZXItZ2lmdC1jZXJ0aWZpY2F0ZXMgY193aXNobGlzdF9ydyBjX2N1c3RvbWVyQ2FydF9ydyBzZmNjLnNob3BwZXItcHJvZHVjdC1zZWFyY2ggc2ZjYy50c19leHRfb25fYmVoYWxmX29mIHNmY2Muc2hvcHBlci1zZW8gY19jb250ZW50X3IgY19wb3B1bGFyU2VhcmNoVGVybXNfciIsInN1YiI6ImNjLXNsYXM6OmJrbnRfcHJkOjpzY2lkOjk5MjQ4MDY3LWYzOWQtNGI4OS04MDZhLWY0NGUxZWQwMzUxNzo6dXNpZDpkMWQ3Zjc1ZC0yMmM3LTQxOGQtODAxOS0xNDVmMGRmYTAwYWQiLCJjdHgiOiJzbGFzIiwiaXNzIjoic2xhcy9wcm9kL2JrbnRfcHJkIiwiaXN0IjoxLCJkbnQiOiIwIiwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JrbnRfcHJkIiwibmJmIjoxNzczOTE1OTkwLCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDphYnE5azRvaFVzMFB4WVJ2MjhaekNWSmdLSDo6c2VzYjpzZXNzaW9uX2JyaWRnZTo6Y2hpZDpjYXJyZWZvdXItYmUiLCJleHAiOjE3NzM5MTc4MjAsImlhdCI6MTc3MzkxNjAyMCwianRpIjoiQzJDMTA3ODY2ODA3MDAtMTI5NzYzMTAxOTE2MjI1MzA1NTg4MDIzMzkzIn0.G8bos9fjeCxPlCzKQ3wXeEaQoGCDu2m66jjdfBeb32OX_4HK1NOyqHPT8f1MMWyUJGPOZfns_4bpLqAZUFlw9g; cc-at_carrefour-be=eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmtudF9wcmQiLCJraWQiOiIxZWQwMWJmNC0zNGQ2LTQxOTAtYTdkNC0zODUzMmEyY2ViZmIiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gY19hdXRoX3Igc2ZjYy5zaG9wcGVyLWV4cGVyaWVuY2Ugc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgY19ib251cy1jYXJkX3Igc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNlc3Npb25fYnJpZGdlIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzLnJ3IGNfY3VzdG9tZXJCYXNrZXRfcncgY19hZGRyZXNzX3IgY19jdXN0b21lck9yZGVyc19yIGNfY2JjX3J3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzIHNmY2Muc2hvcHBlci1jYXRlZ29yaWVzIHNmY2Muc2hvcHBlci1teWFjY291bnQgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RzIHNmY2Muc2hvcHBlci1teWFjY291bnQucncgc2ZjYy5zaG9wcGVyLXN0b3JlcyBjX2NvbmZpZ19yIHNmY2Muc2hvcHBlci1iYXNrZXRzLW9yZGVycyBzZmNjLnNob3BwZXItY3VzdG9tZXJzLnJlZ2lzdGVyIHNmY2Muc2hvcHBlci1teWFjY291bnQuYWRkcmVzc2VzLnJ3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzLnJ3IHNmY2Muc2hvcHBlci1iYXNrZXRzLW9yZGVycy5ydyBzZmNjLn; cc-sg_carrefour-be=1; dwac_49875165c7052266a00c48df9a=uFZRAe_We2k61usYsjZlKWgOWmSUe3JwAWM%3D|dw-only|||EUR|false|Europe%2FBrussels|true; _cs_mk_ga=0.38467956726910113_1773916569719; cqcid=abq9k4ohUs0PxYRv28ZzCVJgKH; cquid=||',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0, i',
}



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)



MONGO_URI = "mongodb://mongotraining:a4892e52373844dc4862e6c468d11b6df7938e16@209.97.183.63:27017/?authSource=admin"

CLIENT = MongoClient(MONGO_URI)
DB_NAME = "carrefour_be_db"
MONGO_COLLECTION_URLS = CLIENT[DB_NAME]["carrefour_be_urls"]
MONGO_COLLECTION_DATA = CLIENT[DB_NAME]["carrefour_be_data"]


def fetch_from_mongo(collection,limit=0,*others):
    projection = {"_id":0}
    if others:
        for field in others:
            projection[field] = 1
    result = []
    for doc in collection.find({},projection).limit(limit):
        result.append(doc)
    return result



FILE_NAME = "carrefour_be_2026_03_24_sample.csv"

FILE_HEADER= [
  "unique_id",
  "competitor_name",
  "store_name",
  "store_addressline1",
  "store_addressline2",
  "store_suburb",
  "store_state",
  "store_postcode",
  "store_addressid",
  "extraction_date",
  "product_name",
  "brand",
  "brand_type",
  "grammage_quantity",
  "grammage_unit",
  "drained_weight",
  "producthierarchy_level1",
  "producthierarchy_level2",
  "producthierarchy_level3",
  "producthierarchy_level4",
  "producthierarchy_level5",
  "producthierarchy_level6",
  "producthierarchy_level7",
  "regular_price",
  "selling_price",
  "price_was",
  "promotion_price",
  "promotion_valid_from",
  "promotion_valid_upto",
  "promotion_type",
  "percentage_discount",
  "promotion_description",
  "package_sizeof_sellingprice",
  "per_unit_sizedescription",
  "price_valid_from",
  "price_per_unit",
  "multi_buy_item_count",
  "multi_buy_items_price_total",
  "currency",
  "breadcrumb",
  "pdp_url",
  "variants",
  "product_description",
  "instructions",
  "storage_instructions",
  "preparationinstructions",
  "instructionforuse",
  "country_of_origin",
  "allergens",
  "age_of_the_product",
  "age_recommendations",
  "flavour",
  "nutritions",
  "nutritional_information",
  "vitamins",
  "labelling",
  "grade",
  "region",
  "packaging",
  "receipies",
  "processed_food",
  "barcode",
  "frozen",
  "chilled",
  "organictype",
  "cooking_part",
  "handmade",
  "max_heating_temperature",
  "special_information",
  "label_information",
  "dimensions",
  "special_nutrition_purpose",
  "feeding_recommendation",
  "warranty",
  "color",
  "model_number",
  "material",
  "usp",
  "dosage_recommendation",
  "tasting_note",
  "food_preservation",
  "size",
  "rating",
  "review",
  "file_name_1",
  "image_url_1",
  "file_name_2",
  "image_url_2",
  "file_name_3",
  "image_url_3",
  "file_name_4",
  "image_url_4",  
  "file_name_5",
  "image_url_5",
  "file_name_6",  
  "image_url_6",
  "competitor_product_key",
  "fit_guide",
  "occasion",
  "material_composition",
  "style",
  "care_instructions",
  "heel_type",
  "heel_height",
  "upc",
  "features",
  "dietary_lifestyle",
  "manufacturer_address",
  "importer_address",
  "distributor_address",
  "vinification_details",
  "recycling_information",
  "return_address",
  "alchol_by_volume",
  "beer_deg",
  "netcontent",
  "netweight",
  "site_shown_uom",
  "ingredients",
  "random_weight_flag",
  "instock",
  "promo_limit",
  "product_unique_key",
  "multibuy_items_pricesingle",
  "perfect_match",
  "servings_per_pack",
  "warning",
  "suitable_for",
  "standard_drinks",
  "environmental",
  "grape_variety",
  "retail_limit"
]