from curl_cffi import requests
from camoufox.sync_api import Camoufox

URL = "https://www.bayut.com/property-market-analysis/transactions/sale/property/?time_since_creation=6m"
API_URL = "https://www.bayut.com/api/transactions"


def get_cookies():
    with Camoufox(headless=False) as browser:
        page = browser.new_page()

        print("Opening page...")
        page.goto(URL, wait_until="domcontentloaded")

        # wait for humbucker challenge to finish
        print("Waiting for challenge...")
        page.wait_for_timeout(15000)

        # get cookies
        cookies_list = page.context.cookies()

        cookies = {c["name"]: c["value"] for c in cookies_list}

        print("\n=== COOKIES ===")
        for k, v in cookies.items():
            print(f"{k} = {v}")

        return cookies


def fetch_api(cookies):
    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en-US,en;q=0.9',
    # # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Referer': 'https://www.bayut.com/property-market-analysis/transactions/sale/property/?time_since_creation=6m',
    # 'Upgrade-Insecure-Requests': '1',
    # 'Sec-Fetch-Dest': 'document',
    # 'Sec-Fetch-Mode': 'navigate',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'Connection': 'keep-alive',
    # # 'Cookie': 'hb-session-id=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..yLAoywRCIIpc80GD.BI5MLvjEZDifGsudeWLIOPZH4SJHEBfZgyEKHMjMiuDOFA_NBTpmkYrn-queOJdLSKXYSi9kABijnkEbWCvOp7E-YEJp0J4c279fjjqKg8KCGQn085RTyy3xgvOwNjiy3nPEN6y04XF4wbdO2ajgGcdz2XizVjMppxkU_JKLGbc_zg66O4WSrS9M-PBDmefbNd9tURp1Kddn3XceM0Bev8f7gKSPSS5I9Z-Bz82IAul_JtnwmH1GyKHghz3VEYlrqWsQX5Lme3CGOy2-X9Li9uaRAZSDrY9G4u_L4Ek5ZhFjXgUe9UPSmv8ncV9_FU89H1V3Yp0R-wCjrjHvo7BlxYAEoQQl3dJSZO3Bi8JrLMZjE6ImyMNnQ1J3JWlBINvEh6ZE7JMVbl4TOQBF7u4d3cVXFOPyHpdux9GFgMzu3Dae8u01Lt6LkEVK7Ltby7wwMw.npVqEX84XIBW-X0ih4H7RA; anonymous_session_id=mncottqqnt7rfzxy; device_id=mncottqqpw4s1fw0; thumb_uid=1a1a1c908c318d8f10bc511238957333; _gcl_au=1.1.895281839.1774844903; _ga_YTDB8TQ5Q9=GS2.1.s1774858846$o4$g1$t1774859459$j59$l0$h0; _ga=GA1.1.1997383460.1774844903; _ga_JMZ5C490RT=GS2.1.s1774858846$o4$g0$t1774858949$j60$l0$h0; _twpid=tw.1774844903624.608341015855002995; _scid=Os2kTwG0O5NvbD73JtWArl_SYMRL8oBN; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22undefined%22%2C%22expiryDate%22%3A%222027-03-30T04%3A28%3A24.438Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22lim8Dl1dyHcdnyVqmcMS%22%2C%22expiryDate%22%3A%222027-03-30T08%3A22%3A30.785Z%22%7D; FPID=FPID2.2.hw1MQQQQd9D7zXlj5BtoTj9MXsfuXlSkAzWO2mVr3jc%3D.1774844903; FPLC=X23BFI%2FxhXbJb6FStG8YO%2BvRnvtypg%2FuS1aLJ9TmHpY73OpNKNfkq9hPNwt4HWg9Sfaqkc3U7T%2BgpSpyuGtZw4mubWzAt6P9T91tGj2iW%2BFEr%2Bu7HSejVPyyqwmsAQ%3D%3D; _fbp=fb.1.1774844905934.959957764291934191; __gads=ID=cac9a859f986fc6a:T=1774844905:RT=1774844905:S=ALNI_MbW8QFQRMIIxEF07XkukjBWUYLeMA; __gpi=UID=00001233fc9b1237:T=1774844905:RT=1774844905:S=ALNI_Mb74dCCmN68I6jYHREB4F4BI7M_hg; __eoi=ID=73ced6b8083d7002:T=1774844905:RT=1774844905:S=AA-AfjZn0wNOdSj_TU5WCMP6rV3c; _tt_enable_cookie=1; _ttp=01KMYG02K8K51K7PY8V3S0XWWX_.tt.1; ttcsid_CFLOJG3C77U9H3ESD14G=1774858848364::p6DQnFOwGzuOMJXkMvzN.4.1774858951804.1; ttcsid=1774858848364::Pfl4JNWtT4mZ-Hre6GFl.4.1774858951804.0; cto_bundle=q_Vcq19kOEwlMkZ2ZGxvczdxb2R6eVFXTUlvdXFEUmxuV3FFTm1pZEpkWVM0a2VUbEJDZ0clMkJxMVp6ZEE0SVV6VkglMkJlYmk2bG43bVo5VU9WQU9iS2JpNk9rUEZlU2hnNTdqQ2YzMm5veXlsVDN2RTVwVHdhSFZ5Rm9KQmRoTFl4N2JlVE1kc2wycE1rb0syQWlVQWJPaENXZVpoQlE1Mm1XOWs3JTJCOG1rTVZqMEpXUWU0QSUzRA; _clck=1ib10gm%5E2%5Eg4s%5E0%5E2280; _sctr=1%7C1774809000000; _clsk=rwp9mj%5E1774859980400%5E77%5E1%5Ey.clarity.ms%2Fcollect; moe_uuid=4f55471a-a63a-45c3-bb5a-a2b6ded67d3b; engag=30; referrer=https%3A%2F%2Fwww.bayut.com%2Fproperty-market-analysis%2Ftransactions%2Fsale%2Fproperty%2F%3Ftime_since_creation%3D6m; original_referrer=https%3A%2F%2Fwww.bayut.com%2Fproperty-market-analysis%2Ftransactions%2Fsale%2Fproperty%2F%3Ftime_since_creation%3D6m; _scid_r=OE2kTwG0O5NvbD73JtWArl_SYMRL8oBN4c2d8Q; _rdt_uuid=1774844903512.af36b8cf-7990-4f3d-98bc-e56397902f83; _uetsid=e48567602bf011f18d33e3e36e12ff74; _uetvid=e48590602bf011f18534ef8b6b532979; abTests=TruBrokerStoriesCarouselTest%255Bv%255D%3Doriginal%26TruBrokerStoriesCarouselTest%255Br%255D%3D1%26SellerLeadsForm%255Bv%255D%3Ddetailed%26SellerLeadsForm%255Br%255D%3D1%26BIScoreAdsIndexTest%255Bv%255D%3Doriginal%26BIScoreAdsIndexTest%255Br%255D%3D1%26WhatsAppProjectLeadIntentQuestionsTest%255Bv%255D%3Doriginal%26WhatsAppProjectLeadIntentQuestionsTest%255Br%255D%3D1%26NaturalLanguageSearchTest%255Bv%255D%3Doriginal%26NaturalLanguageSearchTest%255Br%255D%3D1%26NumberOfTransactionsDTTest%255Bv%255D%3Doriginal20%26InstallAppBannerTest%255Bv%255D%3Doriginal%26InstallAppBannerTest%255Br%255D%3D1',
    # 'Priority': 'u=0, i',
    # }
    page = 1
    json_data = {
        "purpose": "for-sale",
        "categoryExternalID": "1",
        "timeSinceCreation": "6m",
        "sortByFieldName": "date_transaction_nk",
        "sortByFieldOrder": "desc",
        "hitsPerPage": 20,
        "page": 1,
        "v": "5",
    }
    while True:
        response = requests.post(
            API_URL,
            cookies=cookies,
            json=json_data,
            impersonate="firefox135"
        )

        print("\n=== API RESPONSE ===")
        print("page number -- %d",page)
        print("Status:", response.status_code)

        try:
            data = response.json()
            transaction = data.get("hits",[])
            print(transaction)
            page = page + 1
            json_data["page"] = page
        except:
            print(response.text[:500])



cookies = get_cookies()
fetch_api(cookies)
