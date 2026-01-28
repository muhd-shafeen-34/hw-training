
import tls_client
from lxml import html
import json

from settings import INDEX_PAGE_URL, HEADER, logger , save_to_mongo


class CategoryCrawler():
    def __init__(self):
        self.index_url = INDEX_PAGE_URL
        self.logger = logger
        self.header = HEADER
        self.all_category_view_all_links = set()
        self.links_to_save = []

    #this function will extract the view all links of all ccategories

    def _find_view_all_links(self,obj, links):
        if isinstance(obj, str):
            if obj.lower().endswith('view-all.html'):
                if "sale" not in obj.lower() and "new-arrivals" not in obj.lower():
                    links.add(obj)
        elif isinstance(obj, dict):
            for value in obj.values():
                self._find_view_all_links(value, links)
        elif isinstance(obj, list):
            for item in obj:
                self._find_view_all_links(item, links)



  # this is the main method to start crawl on index page to extract links
    def category_crawl(self):
        self.logger.info(f"starting the category crawler on {self.index_url}")
        try:
            data = ""
            session = tls_client.Session(client_identifier="firefox_117")
            response = session.get(self.index_url,headers=HEADER)
            if response.status_code == 200:
                self.logger.info(f"Response fetched successfully : {response.status_code}")
            else:
                self.logger.error(f"Failed to fetch {self.index_url} please change the cookie and tsl_client identifier")

            """this line of code will convert the response.content raw html markup string
               into a structured parsable element tree (DOM)"""

            tree = html.fromstring(response.content)

            """since all the view-all links will load only if we hower on the category tab
              we can find every links in a script tag which is a json formatted file holds Hydration data"""
            
            script = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')
        except Exception as e:
            logger.critical("maybe site got blocked please check response.text")


        if not script:

            self.logger.error(f"No __NEXT_DATA__ script tag found on {self.index_url}")
        try:
            for i in script:
                try:
                        #this will make the script variable into a python dict to ckeck for links

                    data = json.loads(i)

                # This function adds found links to the existing set 
                    self._find_view_all_links(data, self.all_category_view_all_links)
                except json.JSONDecodeError:
                    self.logger.info("Found a script tag that wasn't valid JSON, skipping...")
            self.logger.info(f"Successfully found {len({self.all_category_view_all_links})} links on {self.index_url}")

        except Exception as e:
            self.logger.warning(f"{e}")

        #converting all links from set to list of dict to save to mongo
        self.links_to_save = [{"url":url} for url in self.all_category_view_all_links]
        
        save_to_mongo(self.links_to_save,"category_links")
