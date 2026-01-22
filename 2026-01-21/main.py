import requests
from parsel import Selector
import time
import json
import csv
import tqdm
import re
from urllib.parse import urljoin 

from settings import HEADERS, PARAMS, scraper, url, api_url

class Crawler():
    def __init__(self,url,api_url):
        self.url = url
        self.api_url = api_url
        self.list_of_pdplinks = []
        self.list_agents_details = []

    def start(self):
        #code for fetching the main link response
        print("[INFO] Opening main page...")
        home = scraper.get(self.url,headers=HEADERS)
        print("Warmup status:", home.status_code)
        time.sleep(3)
    #entering to the cms api
        while PARAMS["pageNumber"] <= 46:
            print(f"[INFO] Calling CMS API...{PARAMS['pageNumber']})")
            response = scraper.get(self.api_url, params=PARAMS, headers=HEADERS ,timeout=20)
            print("API status:", response.status_code)
            raw = response.json()
            data = json.loads(raw)
            html = data.get("Html")
            selector = Selector(text=html)
            links = selector.xpath('//a[@class="site-roster-card-image-link"]/@href').getall()
            PARAMS["pageNumber"] += 1
            for i in links:
                if i:
                    self.list_of_pdplinks.append(i)
                else:
                    pass
        for pdplink in tqdm.tqdm(self.list_of_pdplinks, desc="Extracting......"):
            full_pdp_url = urljoin("https://www.alliebeth.com", pdplink)
            details = self.parser(full_pdp_url)
            self.list_agents_details.append(details)
        print(f"parsed {len(self.list_of_pdplinks)} URLs")
        

        self.save_to_csv()
    

    #code for the parser

    def parser(self,full_pdp_url):
        try:
            agent_response = requests.get(full_pdp_url,headers=HEADERS)
            agent_html = agent_response.text
            agent_selector = Selector(text=agent_html)

            #fetching fields

            profile_url = agent_response.url

            #name fetching

            names_fetch = agent_selector.xpath('//div[@class="site-info-contact"]//h2/text()').get()
            if names_fetch:
                names = names_fetch.strip().split()
            else:
                names = []

            first = ""
            middle = ""
            last = ""
            if len(names) == 1:
                first = names[0]
            elif len(names) == 2:      
                first,last = names
            elif len(names) >=3:
                first,middle,last = names[0], names[1], names[-1]

            #image url fetching

            image = agent_selector.xpath('//div[@class="site-bio-image"]/@style').get()

            if image:
                image_url = re.search(r'url\((.*?)\)', image)
                image_url = image_url.group(1) if image_url else None
            else:
                image_url = ""

            #agent phone number fetching

            agent_phone_number = agent_selector.xpath('//div[@class="site-info-contact"]//a[starts-with(@href,"tel:")]/text()').getall()

            #office phone number fetching

            office_raw = agent_selector.xpath('//div[@class="site-info-contact"]//p[contains(.,"Office Phone")]/text()[last()]').getall()
            if office_raw:
                office_phone_number = []
                for i in office_raw:
                    match = re.search(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",i)

                    if match:
                        office_phone_number.append(match.group())
                    else:
                        office_phone_number = []
            
            #description fetching

            description_fetch = agent_selector.xpath('//div[@class="site-about-column"]//div//text()').getall()
            description = ""
            if description_fetch:
                description = " ".join(description_fetch)
            else:
                description = ""
            
            #social and mailid fetch

            mailid_and_social_fetch = agent_selector.xpath('//div[@class="site-info-contact"]//a[starts-with(@href,"https:")]/@href').getall()
            platforms = ['facebook', 'instagram', 'linkedin', 'twitter','youtube','tiktok','pintrest']
            social_links = {}
            cleaned_links = []
            #this field only run when any link returns

            if mailid_and_social_fetch:

                #cleaning social links
                for i in mailid_and_social_fetch:
                    if i not in cleaned_links:
                        cleaned_links.append(i)


                for link in cleaned_links:
                    lower_link = link.lower()
                    for platform in platforms:
                        if platform in lower_link:
                            if platform not in social_links:
                                social_links[platform] = link
                            break
            else:
                pass

                #mail id is not available in the website

            mail_id = "N/A"
        
            social =  social_links

            #fetching address

            address = agent_selector.xpath('//div[@class="site-info-contact"]//p[b]/b/text()').get()

            #fetching office_name 

            office_name = agent_selector.xpath('//div[@class="site-info-contact"]//p[contains(.,"Office Phone")]/text()[last()-1]').get()


            #returning values

            return{
                "profile_url" : profile_url,
                "First_Name" : first,
                "Middle_Name" : middle,
                "Last_Name" : last,
                "Image_url" : image_url,
                "Office_name" : office_name,
                "Address" : address,
                "Description" : description,
                "Social" : social,
                "Maild_id" : mail_id,
                "Agent_phone_numbers" : agent_phone_number,
                "Office_phone_numbers" : office_phone_number,
            }
        except Exception as e:
            print(f"[ERROR] Detail Parsing Failed: {full_pdp_url} -> {e}")


             
    def save_to_csv(self):
        if not self.list_agents_details:
            print("no data to save")
            return
        print("saving data to csv")
        time.sleep(2)
        headers = self.list_agents_details[0].keys()

        with open("data.csv","w",newline="") as file:
            writer = csv.DictWriter(file,fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.list_agents_details)

        print(f"Saved {len(self.list_agents_details)} records successfully")

crawler = Crawler(url,api_url)
crawler.start()
