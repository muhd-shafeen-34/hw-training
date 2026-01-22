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
    "Cookie" : "cf_clearance=IlZNWBwwBi5adCS9qgjVSf4X8WOEyGBKJjGzB21Vxq4-1769056805-1.2.1.1-aODkq5b7yFSd6jFAQJ8oQBQeyNqbybEjHk0HOkQAJ79bxvw0TDQyC6cV.8feL_iCz7hs.WtPE3GvWeWl1n6b6iFVd_NlgFZWub4t7I9mm27uaKEWK0cD5uAbhdXmBWMTvjIOmWCUy7P32K.psRAmLGSSNgDcC.TuB.SA6tXkrub46TI1EGoyI8W03xGxYfmLBq9pCElECHUg8_Ft86pinI7oGamIBjS7qU1rutoBc2XmhiMRdLMng05Dri5MrxCi; culture=en; currencyAbbr=USD; currencyCulture=en-US; _ga_S01P508Z6Z=GS2.1.s1769054547$o8$g1$t1769056805$j60$l0$h0; _ga=GA1.2.1636685237.1768969989; _gcl_au=1.1.805756616.1768969989; _gid=GA1.2.997399669.1768969990; __cf_bm=DyGjtOFCVScVe1Z8dYz4IzS3oFpgWwk_Cpt.5tQ9rlU-1769056798-1.0.1.1-FZrdaStiQ6exlcsl4xBVc6JnDYaT36KnmtKjyFLuI2hf4GnCXFp12TB6bK3UBmhDzrRlQpjtd9DIu8ypexclfb40q7p94LK2NP9QIkiopXw; subsiteID=326373; subsiteDirectory=; ASP.NET_SessionId=vzaup2btkjyxsk4l2arnz3kg; rnSessionID=111147005473380244; _cfuvid=pprUTbkBpGmll0f7B.HChMtCvgb_XNIAlQBhEYLsNyY-1769054545802-0.0.1.1-604800000",
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

