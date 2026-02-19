
import parsel as pq
from urllib.parse import urljoin
import settings
import re
from curl_cffi import requests as rq
class CategoryCrawler():
    def __init__(self):
        self.START_URL = settings.url
        self.header = settings.header
        self.sub_category_links = list()
        self.session = rq.Session()
        self.logger = settings.logger

    def start(self):
        response = self.session.get(self.START_URL,headers=self.header,impersonate="chrome120")
        if response.status_code != 200:
            self.logger(f"website blocked {response.status_code}")
        else:
            self.logger.info(f"website shows {response.status_code}")
        selector = pq.Selector(text=response.text)
        try:
            category_links_fetch = selector.xpath('//ul[contains(@class,"listContainer--xTWe4 bm24--S2oVK")]//@href').extract()
            pattern = re.compile(r"/c/(mens|womens|kids|footwear)(/|$)")
            main_category_links = [urljoin(settings.url,i)for i in category_links_fetch if pattern.search(i)]
            self.logger.info("fetched main url links")
            print(main_category_links)
        except Exception as e:
            self.logger.error(f"website page source is not return in the response text:- {e}")
        
        for main_url in main_category_links:
            try:
                result = self.get_category_links(main_url)
                if isinstance(result,list):
                    self.sub_category_links.extend(result)
                elif isinstance(result,dict):
                    self.sub_category_links.append(result)
            except Exception as e:
                self.logger.error("program failed due to main category loop error %s",e)
        self.logger.info("category crawling completed")
        print(len(self.sub_category_links))
        settings.save_to_mongo(self.sub_category_links,settings.CATEGORY_COLLECTION_NAME)
        




    def get_category_links(self,link):
        """
        Recursively fetches all subcategory links. 
             If no subcategories are found, it assumes it's a listing page.
        """
        try:
            response = self.session.get(link,headers=self.header,impersonate="chrome120")
            selector = pq.Selector(text=response.text)
            sub_cat_fetch = selector.xpath('//a[@data-auid="subCategoryLinks_PLP"]//@href').extract()
            if not sub_cat_fetch:
                #no more categories to go deepnt
                breadcrumbs_fetch = selector.xpath('//span[starts-with(@data-auid, "breadCrumb_link")]//text()').extract()
                breadcrumbs = " > ".join(breadcrumbs_fetch) if breadcrumbs_fetch else ""
                category_name = breadcrumbs_fetch[-1] if breadcrumbs_fetch else ""
                self.logger.info("found category %s with breadcrumb %s",category_name,breadcrumbs)
                self.logger.info(f"found a listing page : {link}")
                return {"category_name":category_name,"breadcrumbs":breadcrumbs,"url":link}
            sub_links = [urljoin(self.START_URL,i) for i in sub_cat_fetch ]
            leaf_category_links = list()
            for url in sub_links:
                #Recursivley going deep
                res = self.get_category_links(url)
                if isinstance(res, list):
                    leaf_category_links.extend(res)
                elif res:
                    leaf_category_links.append(res)
            return leaf_category_links
        except Exception as e:
            self.logger.error(f"RECURSIVE FUNCTION CRASHED due to : {e}")


category = CategoryCrawler()
category.start()





        
    




