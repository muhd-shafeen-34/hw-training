import requests
import parsel
import re
import json
import csv
from urllib.parse import urljoin
     


class CompassAgentCrawler:

    def __init__(self):
        self.base_url = "https://www.compass.com/agents/locations/district-of-columbia-dc/30522/"
        self.session = requests.Session()
        self.current_page = 1
        self.all_agents = []


    #start function of crawler
    def start(self):
        print("[INFO] Compass Agent Crawler Started")

        while True:

            page_url = f"{self.base_url}?page={self.current_page}"
            print(f"[INFO] Crawling Page: {self.current_page}")

            response = self.session.get(page_url)

            if response.status_code != 200:
                print("[ERROR] Page request failed")
                break

            selector = parsel.Selector(response.text)

            agent_links = selector.xpath(".//a[contains(@class,'agentCard-imageWrapper')]/@href").getall()

            if not agent_links:
                print("[INFO] No cards found. Stopping pagination.")
                break

            

            print(f"[INFO] Agents Found: {len(agent_links)}")

            for link in agent_links:
                full_url = urljoin(response.url, link)

                data = self.parse_details(full_url)

                if data:
                    self.all_agents.append(data)

            self.current_page += 1


        print(f"[INFO] Total Agents Scraped: {len(self.all_agents)}")

        self.save_to_json()
        self.save_to_csv()


# code for the parser

    def parse_details(self, url):

        try:
            response = self.session.get(url)
            selector = parsel.Selector(response.text)



            raw_name = selector.xpath(
                "//h1[contains(@class,'profileCard-name')]/text()"
            ).get()

            raw_name = re.sub(r"\s+", " ", raw_name).strip() if raw_name else ""

            first = middle = last = ""

            if raw_name:
                parts = raw_name.split(" ")

                if len(parts) == 1:
                    first = parts[0]
                elif len(parts) == 2:
                    first, last = parts
                else:
                    first, middle, last = parts[0], parts[1], parts[-1]


            

            image = selector.xpath(
                "//img[contains(@class,'profile-image')]/@src"
            ).get()


            

            about_texts = selector.xpath(
                "//div[contains(@class,'profile-about')]//text()"
            ).getall()

            description = ""

            if about_texts:
                cleaned = [t.strip() for t in about_texts if t.strip()]
                joined = " ".join(cleaned)

                description = re.sub(r"\s+", " ", joined)


            

            raw_links = selector.xpath(
                "//div[contains(@class,'profile-experience')]//a/@href"
            ).getall()

            social = {}

            platforms = [
                "facebook", "instagram", "linkedin",
                "twitter", "youtube", "tiktok", "pinterest"
            ]

            url_pattern = re.compile(r"^https?://")

            if raw_links:

                unique_links = list(set(raw_links))

                for link in unique_links:

                    if not url_pattern.match(link):
                        continue

                    lower = link.lower()

                    for platform in platforms:
                        if platform in lower:
                            social[platform] = link
                            break




            email_raw = selector.xpath(
                "//a[contains(@class,'profileCard-email')]/text()"
            ).get()

            email = ""

            if email_raw:
                email_match = re.search(
                    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                    email_raw
                )
                email = email_match.group() if email_match else ""


        
            title = selector.xpath(
                "//div[contains(@class,'titleCard') and contains(@class,'textIntent-body')]/text()"
            ).get()

            title = title.strip() if title else ""


            

            numbers = selector.xpath(
                "//div[contains(@class,'phoneCard')]//a/text()"
            ).getall()

            agent_numbers = []
            office_numbers = []

            for num in numbers:

                clean_number = re.sub(r"[^\d+]", "", num)

                if clean_number:

                    agent_numbers.append(clean_number)

                    if num.strip().startswith("O"):
                        office_numbers.append(clean_number)


            #returninf extracted details

            return {
                "profile_url": url,
                "first_name": first,
                "middle_name": middle,
                "last_name": last,
                "image_url": image,
                "description": description,
                "social": social,
                "email": email,
                "title": title,
                "agent_phone_numbers": agent_numbers,
                "office_phone_numbers": office_numbers
            }

        except Exception as e:
            print(f"[ERROR] Detail Parsing Failed: {url} -> {e}")
            return None


# json saving function

    def save_to_json(self):
        if not self.all_agents:
            print("[INFO] No data to save (JSON)")
            return
        
        with open("agents.json", "w", encoding="utf-8") as file:
            for item in self.all_agents:
                file.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"[INFO] JSON saved: {len(self.all_agents)} records")


# csv saving function

    def save_to_csv(self):
        if not self.all_agents:
            print("[INFO] No data to save (CSV)")
            return

        headers = self.all_agents[0].keys()
    
        with open("agents.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.all_agents)

        print(f"[INFO] CSV saved: {len(self.all_agents)} records")


# starting function

if __name__ == "__main__":
    crawler = CompassAgentCrawler()
    crawler.start()
