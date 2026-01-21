import requests
from parsel import Selector
import time
import cloudscraper
import json
import re
from urllib.parse import urljoin 

url = "https://www.alliebeth.com/roster/Agents"
api_url = "https://www.alliebeth.com/CMS/CmsRoster/RosterSearchResults"

# INFO SET A CUSTOM COOKIE IN THE HEADER BASED ON YOU BROWSER
# IN THE BROWSER DEV TOOL NETWORK TAB THE WESITE REQUEST HEADER COOKIE 


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.alliebeth.com/roster/Agents?__cf_chl_tk=31wyXeHiaidQneuU_GqW16y4Y0tdvp1xKVNTIsVLqrU-1769012710-1.0.1.1-jqnjBYCPPOU61iU3x6SsOYauwuWFJzirbG4SWvSoZZc",
    "Cookie" : "cf_clearance=G.iZ4QJ1hX81Jy19t7VB1l6nfcE1ctEaEsrMYWi4C0c-1769037388-1.2.1.1-SOV6tMY_KThm6pf7_XwoMlKz0R9p_ulzQ0xdAvLwaT7YUX5ZmrK08zmEObGJTITGF1QbAm48BvpKpAjy1nTEvHAnXvIrbtabMA6WRCplon4tUCCpcXuqrlmgVBqNHVPi2FJyuBC7VKZhJpcp4oNr1vJ5K11_BNm04rm0OPiJLHIhVRvj.UMuNggSQvUnRr9hhtlPnUYPcDp31zCRISUHgGMdjmNnNjO7tsS6bPSkyXeEpwvZwYSrT3eivXn8lFco; culture=en; currencyAbbr=USD; currencyCulture=en-US; _ga_S01P508Z6Z=GS2.1.s1769031666$o6$g1$t1769037401$j50$l0$h0; _ga=GA1.2.1636685237.1768969989; _gcl_au=1.1.805756616.1768969989; _gid=GA1.2.997399669.1768969990; _cfuvid=Mc3SBTGZ48XjHiz6hslF5K4UUWXWt78Xy9izHjon5Qw-1768977447225-0.0.1.1-604800000; subsiteID=326373; subsiteDirectory=; ASP.NET_SessionId=hhyjgajhfkuowmosk4ky3ro3; rnSessionID=619612531765993812; __cf_bm=C3QjeMd1CWgE19I0PRzVWbsPA2yJOI1mQ0Owq1arBKk-1769037097-1.0.1.1-zRqeuXd00O_PL.Xx8h0fPZ8u0fT7ntuKb9rwoqBZdEgf8ClOFOlrOQFZn_OY9PYa3wFzu.5R8mR4vvoHbWKQOF_L8MLsUlImxts3Rq87qJc",
}



PARAMS = {
    "layoutID": 1081,
    "pageSize": 10,
    "pageNumber": 1,
    "sortBy": "firstname-asc"
}

scraper = cloudscraper.create_scraper(
    browser= {
        "browser" : "chrome",
        "platform" : "windows",
        "desktop" : True

    }
)

