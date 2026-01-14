import requests
from bs4 import BeautifulSoup
from settings import URL, RAW_HTML_FILE, CLEANED_DATA_FILE, extract_details #imported regex function 


class DataMiningError(Exception):

    pass


class CompassParser:
    def __init__(self, url):
        self.url = url
        self.html = ""
        self.cleaned_list_items = []

    def __del__(self):
        self.close()

    def start(self):
        print(f"Starting crawler for {self.url}")
        self.fetch_html()
        self.parse_item()
        self.save_to_file()

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.html = response.text

            with open(RAW_HTML_FILE, "w") as file:
                file.write(self.html)

            print("HTML FILE Created and saved")

        except requests.RequestException as error:
            print(f"[ERROR] Fetch failed: {error}")
            raise

    def parse_item(self):
        try:
            raw_list = self.parse_data()


            self.cleaned_list_items = [ extract_details(text) for text in raw_list ]
            
            # self.cleaned_list_items = self.parse_data()
            list_of_names = [names["name"] for names in self.cleaned_list_items]


            print(f"Parsed {len(self.cleaned_list_items)} valid details")
            print(list_of_names)

        except Exception as error:
            raise DataMiningError(f"Parse item failed due to: {error}")

    def parse_data(self):
        self.details = []
        soup = BeautifulSoup(self.html, "html.parser")
        cards = soup.find_all("div", class_="agentCard")

        if not cards:
            raise DataMiningError("No agent cards found")

        for card in cards:
            self.cleaned_text = card.get_text(separator= " ",strip= True).replace("\n","")
            self.details.append(self.cleaned_text)
        return self.details

    def save_to_file(self):
        with open(CLEANED_DATA_FILE, "w") as file:
            for item in self.cleaned_list_items:
                file.write(f"{item}\n")

        print("[SUCCESS] Cleaned data saved")

    def yield_lines_from_file(self):
        with open(CLEANED_DATA_FILE, "r") as file:
            for line in file:
                yield line.strip()


    def close(self):
        print("[INFO] Parser closed")

parser = CompassParser(URL)
parser.start()

print("\n[PRINTING DATA FROM A FILE USING GENERATOR]")
for line in parser.yield_lines_from_file():
    print(line)
