import requests as rq
from pathlib import Path
import logging
from pymongo import MongoClient,UpdateOne
# header = {
     
#      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#      "Accept-Encoding":"gzip, deflate, br, zstd",

#     "Accept-Language":"en-US,en;q=0.9",
#     "Connection":"keep-alive",

#    "Host":"www.academy.com",
#     "Referer":"https://www.academy.com/c/mens?&facet=%27facet_Price%27:%3E%20500",
#     "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
# }   

header = {
"Host": "www.academy.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "",
"Connection": "keep-alive",
"Cookie": """mt.v=2.1490160728.1770881436242; _ALGOLIA=anonymous-9d931812-b28b-426c-9a58-6e90d87a1763; c_uuid=25011866414702010010114705864153624; _pxhd=hAeM-0zGNAmVxUa30X42yDFDLGcoEzfy6hWUkDKnTrJo31kQBsZhOqwNxUMlIZPy6y08ETVbXauZtoFjN5YDdw==:ihTL5BdZnqLidMplNgtVPHYiKE1vAoonG-9mVPpHNiOV5h6A481Tc5ytNydV4/PqWBychZz5tArOyxXPEODwmtEKwAYx77FNmisnc2sfxvU=; utag_main_v_id=019c50c250ab00188be1bfbf1e240504e001801100978; utag_main__sn=23; utag_main_vapi_domain=academy.com; AMCV_606441B5546CD33C0A4C98A7%40AdobeOrg=179643557%7CMCIDTS%7C20501%7CMCMID%7C66473696578073377111461077236448016395%7CMCAAMLH-1771948615%7C12%7CMCAAMB-1771948615%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1771351015s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-20504%7CvVersion%7C5.5.0; utag_main_dc_visit=23; s_nr30=1771343839041-Repeat; s_nr365=1771343839041-Repeat; s_tslv=1771343839042; s_vnc365=1802879814800%26vn%3D23; _gcl_au=1.1.17534692.1770881439; _pxvid=b9caec3f-07e4-11f1-a685-644e3e017826; atgRecVisitorId=1102eOZ73PymO_OJjf3ua6ZzccPyis142D1vYy6TU7lV5JU94BA; s_ecid=MCMID%7C66473696578073377111461077236448016395; crl8.fpcuid=d1036eba-67c6-4e93-bd8f-21e7d81b41d7; _fbp=fb.1.1770881447598.242294197950624794; academy_clarip_consent=0,1,2,3; GSIDc6dmlqeqKI30=ce6c827a-c895-4a08-90cc-114321ee5bae; STSIDc6dmlqeqKI30=af2f28a3-fe30-4844-ac33-903d3f2a19d8; _br_uid_2=uid%3D7919352159444%3Av%3D17.1%3Ats%3D1770881457824%3Ahc%3D483; QuantumMetricUserID=e8ac2f0087551261d584e6459fa0d2ff; styliticsWidgetSession=79d9b532-c42b-4423-b701-74ee82a0f115; BVBRANDID=65e2abf4-8cdf-4690-9001-d2e5f95e6a4d; s_fid=30E39541909AEFB9-0BAAE53F05501B5A; s_vi=[CS]v1|34C6C8975BB2955E-40000847A0221E17[CE]; aso.audience.Running=Kids; fw_se={%22value%22:%22fws2.3fb0450e-d985-4086-947d-80ff9f0c23a6.15.1771318335541%22%2C%22createTime%22:%222026-02-17T08:52:15.542Z%22}; fw_uid={%22value%22:%2266d13967-b8e9-41e4-b6b0-4e70159a2bf8%22%2C%22createTime%22:%222026-02-17T08:52:15.543Z%22}; fw_bid={%22value%22:%225LNmzk%22%2C%22createTime%22:%222026-02-17T08:52:16.768Z%22}; contentstack=true; akamai_ch=A; cscv=default; dtCookie=v_4_srv_8_sn_3C5314EC1748231FBCA2B858A506438F_perc_100000_ol_0_mul_1_app-3Ac941cf92b69f2e35_0; USERTYPE=G; enablePriceRangeAttributes=true; enableShowPriceSwatch=true; klarnaTender=true; dMOnQV=true; ACADEMY_PLCC_USER=true; cscvCookieEnabled=true; lcontentstack=ckt|ord|act; atClEn=false; guestFavorite=true; ecp=Y:Y:Y; enableXCCPromotion=true; iaf=nbm; akaalb_Default-ALB-production=1771345589~op=wwwDefaultALB:PROD1EAST|~rv=94~m=PROD1EAST:0|~os=b7cd39262b6e2f76bba2f46a7a88a486~id=68bda240da8002b5e68dd37546681046; akavpau_wd=1771344444~id=b278983935d0e8cd79c6438803f9ac87; pxcts=3bc06c36-0c19-11f1-ae86-7e7ff04caa64; _px3=109142bdaa504da357b794943416abcc8a723bb6487e141568312148b6a594bd:8GxoRw15SGozW+gSNXOFoTNzO9Bg+PKcuXeQuubEtASaB/qi7lZxHwrAK294nhtyCi0b1e1aRCplCWNZlYZ4ug==:1000:Wqk/XOucoLaUxtzdqYxCZNNKbdEOIqundT157/gsTbJxQEFZfhvY4YM0GmT2B972mNu+iL4HtL8Baagc6NqKyWWSqWaPzaf5Y8/0eiJmfVyv0na6au4YY0AMHHvu0P57MyfAlETU/4mQVXS3PticXlhjKW60MV3zDBUBp8EfVYbeYCVDZIpTP60ShQFzCPqbs66a1hYy4v1UW6JGzybBjtxArvJTIFh9UavZu4HO9ELIn1EWYYeoCzut/1RCLEa3iaWalSnTL/+wsmHmDz/JWgwFc6umOs8JMvE/EBxfRzMgCxVh0qwWpbUiVqW2yVxlEljeZ/I+TiSLhmizLZmkUPeTmuBv2CUmu3+AJxje4IMvur17XaYJVuBY0yqkH0lz0a+HkCCx6LV/yvqhJCXFCASWqoJvwTGFJEy10tejoGFUjJYI9SWBnSrC7i8Xvka/dWA3cSb16QwrZhjG27jVTYzXeHZObOpHig7UnkWcFmE=; correlationId=AA-B2Rhi6P4aVF2MnJ5BYleTJFU97FULwH2; utag_main__se=5%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__st=1771345638790%3Bexp-session; utag_main_ses_id=1771343813704%3Bexp-session; utag_main__pn=3%3Bexp-session; utag_main_academy_visitorId=guest%3Bexp-session; LAT_LONG=9.97,76.23; xdVisitorId=1102eOZ73PymO_OJjf3ua6ZzccPyis142D1vYy6TU7lV5JU94BA; sddStoreId=; utag_main__prevpage=https://www.academy.com/%3Bexp-1771347438801; s_inv=7313; s_ivc=true; utag_main_dc_event=4%3Bexp-session; AMCVS_606441B5546CD33C0A4C98A7%40AdobeOrg=1; s_ips=391; s_tp=3902; s_cc=true; atgRecSessionId=jo1sUaGC-aX2jQ3Bd3OrbrobT0e0KU-CvaibLGiKW60Y4h92fBgZ!-1735488247!-141976494; utag_main_dc_region=me-central-1%3Bexp-session; utag_main_qm_replay_sent=1771343813704%3Bexp-session; ltkSubscriber-Signup=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; ltkSubscriber-GXPMonetate=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; QuantumMetricSessionID=6c76717c45a42c784f54501a11abe3b8; s_sq=%5B%5BB%5D%5D; s_ppv=academy%2C17%2C10%2C678%2C1%2C9; _uetsid=cd7cb9800af011f18f8cc9f8e64a3072; _uetvid=bf4577a007e411f1a5996f9d0e995a16; _vuid=8a449c81-8ad7-49d1-aeae-42d02689e16c""",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=0, i",
"TE": "trailers",
}




url = "https://www.academy.com/"


MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "academy_poc_2026_02_16"
CATEGORY_COLLECTION_NAME = "academy_product_category_urls"
PDP_URLS_COLLECTION_NAME = "academy_product_pdp_urls"




LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "academy.log"

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),

    ]
)

logger = logging.getLogger("academy_scraper")


def save_to_mongo(data, collection_name):
    if not data:
        print("No data provided to save.")
        return

    try:
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][collection_name]
        collection.create_index("url", unique=True)

        operations = [
            UpdateOne(
                {"url": doc["url"]},
                {"$set": doc},
                upsert=True
            )
            for doc in data
            if "url" in doc
        ]

        if not operations:
            print("No valid documents to insert.")
            return

        result = collection.bulk_write(operations, ordered=False)
        print(
            f"Matched: {result.matched_count} | "
            f"Upserted: {len(result.upserted_ids)} | "
            f"Modified: {result.modified_count}"
        )

    except Exception as e:
        logger.exception("Mongo save failed due to : %s",e)



def fetch_from_mongo(collection_name):
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][collection_name]

    urls = [
        doc["url"]
        for doc in collection.find({}, {"_id": 0, "url": 1})
    ]

    return urls
# response = rq.get(url,headers=header)
# print(response.status_code)
# print(response.text)