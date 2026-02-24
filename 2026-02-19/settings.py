from pymongo import MongoClient
from pathlib import Path
import logging

start_url = "https://find.reelly.io"


header = {
    "Host": "find.reelly.io",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Cookie": """_ga_FLEWD7XJW4=GS2.1.s1771491024$o2$g1$t1771491268$j60$l0$h0; _ga=GA1.1.2073224037.1771476101; _gcl_au=1.1.1347252921.1771476101; _ga_SG8FHQK16D=GS2.1.s1771494802$o3$g1$t1771495154$j57$l0$h0; _lfa=LF1.1.8913ac964e1e9633.1771476102029; _ga_84VT17GZ4P=GS2.1.s1771491024$o2$g1$t1771491268$j60$l0$h0; _tt_enable_cookie=1; _ttp=01KHT38BTH8AYF2E8QFNQGJXNY_.tt.1; ttcsid_D4SIA63C77U3O2FSI9R0=1771494805819::Y0f5Z1km_cl_k8uiXM7J.3.1771495154295.1; ttcsid=1771494805819::jnN6_qJ7rOjyPqVwYqP9.3.1771495154295.0; _hjSessionUser_3072403=eyJpZCI6IjRhNGE4YWZkLTA3OWUtNWYyZi1hOWI5LTcxMWI5MTg5YWYxZSIsImNyZWF0ZWQiOjE3NzE0NzYxMDMwMDMsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1771476103023.614790307381912208; _clck=v5ka45%5E2%5Eg3p%5E0%5E2241; _hjSessionUser_3296711=eyJpZCI6ImMzYmIzYTkyLTVjODgtNWZmOC1hMTRlLTg3NGNmN2ViYTY1YSIsImNyZWF0ZWQiOjE3NzE0NzYxMDg0MDAsImV4aXN0aW5nIjp0cnVlfQ==; auth_token=eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.EifbiFvSMGU7YC-KwVIJZKie2ofGvndBHX9TTSSm0KAQPNOojpBBOoCNlLTq_f2-tP3PnRN2zV-tAx3OHG76bRP2qa-VdAAE.o-cDkillYQxbkNbQiXDHTw.7yTuSaNufpZl4uD2mesCzl5iWLJl9J4XgqAsI-ORpSgUgccD5_u51oStdqLjSKU0-4OlWlOlnvDlTqi-g4B-9hfjw3A6iC_z752So_oKnKmwMp7QoWLimQAfq2_t6dGBKr2bOXWGR9FPmo0zO021J9R20Jiih5bU-HsEZlkbJMs.HMYeFd2cQtDrofYLD37SPfKwo5npg8e8FN6ENhU_BV4; _clsk=zakqs1%5E1771495154741%5E21%5E1%5Ei.clarity.ms%2Fcollect; _hjSession_3072403=eyJpZCI6IjJhNTE5OWYyLTgyNGItNDE1My1hOThkLTM3N2M0MDMwODgyNSIsImMiOjE3NzE0OTEwMjgyMDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; intercom-id-e85yq5qw=948eeb64-33cc-4571-8531-fc967954e4e0; intercom-session-e85yq5qw=NDNGb2hlODFQbTdFUWpnRXhjTVcvMlorY05sYWhhRlNKbE91ZE9RekFLNTkrN1NIQ1ZDa21aRzBoOWdTVGFEK1laVjI2Mno4Qy9OTUdXWGQ0TVFSQmpUL2NUOVdyT3pyS3ZpQUpxMHNkY3lDWXJRQm9RVU9WY09tR0tyWVpGMkVGeFRkUlJWYXpDQ3BRRkVBVW5xSTZRT3FMbm1BT1VWWnJVMXBJd1R2YWtxSTlwbGVMaEV0aWNQZ0tyWk44OG9mLS1YTUJ0TW5GYXhkYjNVTHdXVWp0MFRBPT0=--c0f41e1f0eedbd113fc5a13af43684d66499e624; intercom-device-id-e85yq5qw=a0b9c150-b0b4-4fda-9590-52c66e1c6bd9; mp_a7048914da26961e15e03cb1c6f00348_mixpanel=%7B%22distinct_id%22%3A%2264488%22%2C%22%24device_id%22%3A%228f4dd9f4-587c-44b9-bbad-b0345e816a04%22%2C%22utm_source%22%3A%22reelly_platform%22%2C%22utm_medium%22%3A%22user_id%3D36227%22%2C%22utm_campaign%22%3A%22undefined%22%2C%22utm_content%22%3A%22undefined%22%2C%22utm_term%22%3A%22undefined%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fsoft.reelly.io%2F%22%2C%22%24initial_referring_domain%22%3A%22soft.reelly.io%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22Environment%22%3A%22Native%20Production%22%2C%22%24user_id%22%3A%2264488%22%7D""",
    "Upgrade-Insecure-Requests":"1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Priority": "u=0, i",
    "TE": "trailers",
    }


params = {

			"pricePer": "unit",
			"preferredAreaUnit": "sqft",
			"withDealBonus": "false",
			"handoverOnly": "false",
			"handoverMonths": "1",
			"postHandoverMin": "10",
			"preHandoverMax": "100",
			"onlyPostHandover": "false"
}


api_url = "https://api-reelly.up.railway.app/api/internal/projects"

product_api = "https://api-reelly.up.railway.app/api/internal/projects"

	
api_params =  {
    "limit":"50",
    "offset":"50", 
        "preferred_area_unit": "sqft",
        "sorting_seed": "8011f547-8cd0-4afb-b377-fc818c0ad544"

    }


api_header = {
"Host": "api-reelly.up.railway.app",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
"Accept": "application/json, text/plain, */*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://find.reelly.io/",
"content-type": "application/json",
"xano-authorization": """eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.EifbiFvSMGU7YC-KwVIJZKie2ofGvndBHX9TTSSm0KAQPNOojpBBOoCNlLTq_f2-tP3PnRN2zV-tAx3OHG76bRP2qa-VdAAE.o-cDkillYQxbkNbQiXDHTw.7yTuSaNufpZl4uD2mesCzl5iWLJl9J4XgqAsI-ORpSgUgccD5_u51oStdqLjSKU0-4OlWlOlnvDlTqi-g4B-9hfjw3A6iC_z752So_oKnKmwMp7QoWLimQAfq2_t6dGBKr2bOXWGR9FPmo0zO021J9R20Jiih5bU-HsEZlkbJMs.HMYeFd2cQtDrofYLD37SPfKwo5npg8e8FN6ENhU_BV4""",
"Origin": "https://find.reelly.io",
"Connection": "keep-alive",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "cross-site",
"Priority": "u=4",
"TE": "trailers",
}


MONGO_URI = "mongodb://mongotraining:a4892e52373844dc4862e6c468d11b6df7938e16@209.97.183.63:27017/?authSource=admin"
client = MongoClient(MONGO_URI)
DB_NAME = "reelly_io_db"
PDP_URLS_COLLECTION = client[DB_NAME]["reelly_urls"]
MONGO_COLLECTION_DATA = client[DB_NAME]["reelly_data"]


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "reelly.log"

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),

    ]
)

logger = logging.getLogger("reelly_scraper")


def fetch_from_mongo(collection, *others):

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



FILE_NAME = "reelly_2026_02_19_sample.csv"
FILE_HEADERS = ["unique_id","url","name","price","image_url","status","developer","unit_types","district","description"]




#user details

# {
# 	"id": 64488,
# 	"early_access": false,
# 	"old_offplan_tab": false,
# 	"name": "sha",
# 	"email": "reyland.moxley@flyovertrees.com",
# 	"phone": "+9712495378460",
# 	"company": "gfgf.com",
# 	"companyLegalName": 0,
# 	"lastActivity": 1771491272765,
# 	"created_at": 1771491264576,
# 	"customer_id": "",
# 	"advisor_token": "",
# 	"Paid": "",
# 	"payment_type": "",
# 	"Status": "New",
# 	"Comments": [],
# 	"pointsBalance": 0,
# 	"subEndDate": 1771491264574,
# 	"lastModified": 1771491264574,
# 	"role": "Broker",
# 	"position": "Seller",
# 	"agents_in_company": "2-5",
# 	"referralsForPeriod": 0,
# 	"referrals": [],
# 	"TelegramLink": "",
# 	"referrer": 0,
# 	"referralsCount": 0,
# 	"invitesBalance": 5,
# 	"Ref_ID": "486a6b70-da87-4036-a0c7-27226a4f7942",
# 	"whenJoinedCompany": "",
# 	"license": "",
# 	"licenseIssueDateInput": "",
# 	"social": "",
# 	"languages": [],
# 	"country": "India",
# 	"city": "",
# 	"instagramLink": "",
# 	"instFollowers": 0,
# 	"manychatInst": "",
# 	"ManychatTelegram": "",
# 	"lastProjectId": 0,
# 	"responsible": "",
# 	"projects_views": 0,
# 	"qr": "",
# 	"company_website": "",
# 	"generated_offers": 0,
# 	"popup_result": 0,
# 	"profileImage": null
# }