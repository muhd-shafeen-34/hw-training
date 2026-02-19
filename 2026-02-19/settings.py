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
"Cookie": """_vuid=d9caa3b9-20a0-4e3a-a3e6-921102348d47; mt.v=2.1490160728.1770881436242; _ALGOLIA=anonymous-9d931812-b28b-426c-9a58-6e90d87a1763; c_uuid=25011866414702010010114705864153624; _pxhd=OnTS8tmWCfjKfQTIKayRtI6wunOhzFWEC6uD1BvQxUq7O8gnOFIdch6f5KQE0-cIyxYPJ4Z7pVeev4UP0ZXLpQ==:XtmUvQwihXkeSfHdD7/YExAolJl70n32S8t8mBNz6gfMC3F9Yo9kA4VlIhzpbZYvK6DL9RuzLKatVHukjkYDo4VYNuOmgg5di7n7DePCFL0=; utag_main_v_id=019c50c250ab00188be1bfbf1e240504e001801100978; utag_main__sn=30; utag_main_vapi_domain=academy.com; AMCV_606441B5546CD33C0A4C98A7%40AdobeOrg=179643557%7CMCIDTS%7C20503%7CMCMID%7C66473696578073377111461077236448016395%7CMCAAMLH-1772087736%7C12%7CMCAAMB-1772087736%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1771490136s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-20511%7CvVersion%7C5.5.0; utag_main_dc_visit=30; s_nr30=1771483561742-Repeat; s_nr365=1771483561742-Repeat; s_tslv=1771483561743; s_vnc365=1803018933981%26vn%3D30; _gcl_au=1.1.17534692.1770881439; _pxvid=b9caec3f-07e4-11f1-a685-644e3e017826; atgRecVisitorId=1102eOZ73PymO_OJjf3ua6ZzccPyis142D1vYy6TU7lV5JU94BA; s_ecid=MCMID%7C66473696578073377111461077236448016395; crl8.fpcuid=d1036eba-67c6-4e93-bd8f-21e7d81b41d7; _fbp=fb.1.1770881447598.242294197950624794; academy_clarip_consent=0,1,2,3; GSIDc6dmlqeqKI30=ce6c827a-c895-4a08-90cc-114321ee5bae; STSIDc6dmlqeqKI30=af2f28a3-fe30-4844-ac33-903d3f2a19d8; _br_uid_2=uid%3D7919352159444%3Av%3D17.1%3Ats%3D1770881457824%3Ahc%3D546; QuantumMetricUserID=e8ac2f0087551261d584e6459fa0d2ff; styliticsWidgetSession=79d9b532-c42b-4423-b701-74ee82a0f115; BVBRANDID=65e2abf4-8cdf-4690-9001-d2e5f95e6a4d; s_fid=30E39541909AEFB9-0BAAE53F05501B5A; s_vi=[CS]v1|34C6C8975BB2955E-40000847A0221E17[CE]; aso.audience.Running=Women; USERTYPE=G; akamai_ch=A; enablePriceRangeAttributes=true; enableShowPriceSwatch=true; ACADEMY_PLCC_USER=true; akavpau_wd=1771484166~id=dbbe49eeb193caf395aa3c4a69800a6b; dtCookie=v_4_srv_5_sn_UGCBBLBS4DN2STCBTRIU5NKRDSAEOQDC_perc_100000_ol_0_mul_1_app-3Ac941cf92b69f2e35_0; rxVisitor=1771474190986UG9KBMOBL95RFUM349F42GFSG3VHGBJH; dtPC=-26932$274190983_390h11vEEEKHGJANFUHNBCSPIVWHAATJEMHPMMJ-0e0; rxvt=1771475993183|1771474190987; LAT_LONG=43.12,5.94; xdVisitorId=1102eOZ73PymO_OJjf3ua6ZzccPyis142D1vYy6TU7lV5JU94BA; sddStoreId=; cscv=default; AMCVS_606441B5546CD33C0A4C98A7%40AdobeOrg=1; s_ips=1558.5999755859375; s_tp=3786; s_cc=true; atgRecSessionId=YjJ0nGnmS5DadcUttxWOWBSywckPpWmICgI1G4jn3BGY8Efi90GZ!1730718653!-1556203499; pxcts=d882f4db-0d48-11f1-b767-e3b0568e96fe; _px3=76b43f7fb532777dd254842284935d54029e2256d9e1168588e7fb7d65f0a125:c4q+IQ52oZCo8InoxctOQ6TVndw4ryUjmJeY08TmZUgzOLNIWWmmLd3xp3Vb8oABv0AsAH0+Iki2aAHPm3idyw==:1000:0ovha4v2g3pZm1IVM4UJAIu/x61LkeuxbhDP2Pep7QET5Tq4W/SWN+OvSTyvqjFBlTctJGTS7wJE/I9WKZ70PoN2118NkZg/Luzp0/0yLfiEtcdTmyADKuRF1Ai/cURpnRC8ND2CzOQNOOq/Pjn/Z1pN86sPMD6gZoxtIussyz1xZImSQOILHY2eNU2XKNUwaSnDyyEMAu26vRqS7hpjGr9Fpvv5Goh59ZetKC0qpGfPINh896kf9q+SVnhhBxW7/G4eMwUPVayZnEqKbb8h2PpfjjkYYiDWfhgKcnHqe4ISrrNAt/3nup8YDANKdLReD87Q5GibbgazauUpqCK6+ONKs8ZVQZulCDKC6zsl1YDDRGeKiEEacmSOpWMwm+aW1rmZYXEW0rrTbFfhhSn4FTZnk+7RRi0zSjrdCUQzB+G/xZuhiyb2/7sZjGyXmAHc5hIbIqMnGQpdt2BTMP23QkRPHJBY718mo+vZ4vwimfw=; ltkSubscriber-Signup=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; ltkSubscriber-GXPMonetate=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; s_sq=%5B%5BB%5D%5D; contentstack=true; JSESSIONID=0000-DdChXHVw29q9IAdr_mEFn1:1cgetcj18; WC_PERSISTENT=%2BWPtT0%2FH0HtF12c82PN%2FVP9inR8bpsdfPLmcEJRFMcs%3D%3B2026-02-18+23%3A09%3A18.043_1771477757965-98854_10151_2797222710%2C-1%2CUSD%2CzFf3Lfgg4gXEF06UmvoKZEkLWWV7%2B4DyQ4EIVrMj6UdygqlrdskdBkrhyzWPkWlNQW75v13s6foCQRkV0OZ7lQ%3D%3D%2C2026-02-18+23%3A09%3A18.043_10151; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_2797222710=2797222710%2CsRkquXcpnoXjhJOIzGRpC6NESHd06sSO5GrmadylNXw%3D; WC_ACTIVEPOINTER=-1%2C10151; WC_USERACTIVITY_2797222710=2797222710%2C10151%2Cnull%2Cnull%2C1771477758046%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1820917278%2CpbSahkEO%2Bm4q85EJ30r4XfItqK5G2pto8pUdGO68s38edoyl4SzXD33ey%2B%2Fa%2F5f5g7%2Br2FO6wd224dA1Am0pQ1k5xbaRYQEfAfG%2BAKjqDps8ILFbRJq1ssVsWw5YkJr7Dj5HBKvjcxtUIzEm2v7ACp6h%2BdVM8lM6hOvySfIdUS6AiYEh5pxY4WaE0kfNl4HVSQxq8Zoxa%2F1wKiVCOs1sOQJKcS%2BhvHE%2FAQP%2Fz%2BHqoaryfxeJpiBjMrWJ8E3YC4I8euhzofZ6L8%2BVcpP6wvXgYw%3D%3D; USERACTIVITY=2797222710; channel=-; klarnaTender=true; dMOnQV=true; cscvCookieEnabled=true; lcontentstack=ckt|ord|act; atClEn=false; guestFavorite=true; ecp=Y:N:Y; enableXCCPromotion=true; iaf=nbm; akaalb_Default-ALB-production=1771484730~op=wwwDefaultALB:PROD1EAST|~rv=28~m=PROD1EAST:0|~os=b7cd39262b6e2f76bba2f46a7a88a486~id=6912699dedbdbb113d40699dbc3bee14; BVBRANDSID=8243cff0-3e58-4c6d-9e78-2ea6f398117c; utag_main__se=4%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__st=1771485361732%3Bexp-session; utag_main_ses_id=1771482932173%3Bexp-session; utag_main__pn=1%3Bexp-session; utag_main_academy_visitorId=guest%3Bexp-session; correlationId=AA-QbBGoijFeBBhRjImOIA5NjHuPSVyRbzl; utag_main__prevpage=https://www.academy.com/p/bcg-mens-coaches-polo-shirt-129381334%3Bexp-1771487161737; s_inv=4591; s_ivc=true; utag_main_dc_event=4%3Bexp-session; utag_main_dc_region=me-central-1%3Bexp-session; s_ppv=bcg%2520mens%2520coaches%2520polo%2520shirt%2520%257C%2520academy%2C42%2C41%2C1579%2C1%2C5; fw_se={%22value%22:%22fws2.4e86708a-8b1e-4ad6-bb7e-c45874266559.28.1771482936399%22%2C%22createTime%22:%222026-02-19T06:35:36.399Z%22}; fw_uid={%22value%22:%2266d13967-b8e9-41e4-b6b0-4e70159a2bf8%22%2C%22createTime%22:%222026-02-19T06:35:36.400Z%22}; fw_bid={%22value%22:%225LNmzk%22%2C%22createTime%22:%222026-02-19T06:35:36.855Z%22}; utag_main_qm_replay_sent=1771482932173%3Bexp-session; _uetsid=cd7cb9800af011f18f8cc9f8e64a3072; _uetvid=bf4577a007e411f1a5996f9d0e995a16; ltk-product-QOH=210; QuantumMetricSessionID=ecabea84838fd9c07a73a761e611e03c""",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=0, i",
"TE": "trailers",
}

url = "https://www.academy.com/"



FILE_NAME = "academy_2026_02_19.csv"

FILE_HEADERS = [
    "unique_id", "url", "product_name", "brand", "selling_price",
    "regular_price", "discount", "description", "specification",
    "fit_type", "image", "rating", "review", "size", "colour"
]

# api_url = "https://apps.bazaarvoice.com/bfd/v1/clients/Academy/api-products/cv2/resources/data/reviews.json"

# review_api_header = {
#     "Host": "apps.bazaarvoice.com",
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
#     "Accept": "*/*",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Referer": "https://www.academy.com/",
#     "Bv-Bfd-Token": "9102,main_site,en_US",
#     "Origin":"https://www.academy.com",
#     "Connection": "keep-alive",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "cross-site",
#     "Priority": "u=4",
#     "TE": "trailers",
# }

# def get_bv_review_params(product_id, offset=0, limit=5):
#     return {
#         "resource": "reviews",
#         "action": "REVIEWS_N_STATS",
#         "filter": [
#             f"productid:eq:{product_id}",
#             "contentlocale:eq:en_US,en_US",
#             "isratingsonly:eq:false"
#         ],
#         "filter_reviews": "contentlocale:eq:en_US,en_US",
#         "include": "authors,products,comments",
#         "filteredstats": "reviews",
#         "Stats": "Reviews",
#         "limit": limit,
#         "offset": offset,
#         "limit_comments": 3,
#         "sort": "submissiontime:desc",
#         "apiversion": "5.5",
#         "displaycode": "9102-en_us"
#     }








MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
DB_NAME = "academy_poc_2026_02_16"
CATEGORY_COLLECTION_NAME = "academy_product_category_urls"
PDP_URLS_COLLECTION_NAME = "academy_product_pdp_urls"
MONGO_COLLECTION_DATA = client[DB_NAME]["academy_product_data"]







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



def fetch_from_mongo(collection_name, *others):
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][collection_name]

    # Base projection
    projection = {"_id": 0, "url": 1}

    # Add optional fields
    for field in others:
        projection[field] = 1

    results = []

    for doc in collection.find({}, projection):
        if others:
            item = {"url": doc.get("url")}
            for field in others:
                item[field] = doc.get(field)
            results.append(item)
        else:
            results.append(doc["url"])

    return results
