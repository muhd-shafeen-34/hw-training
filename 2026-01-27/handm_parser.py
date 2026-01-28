import parsel as pq
import tls_client
import re
from urllib.parse import urljoin
import random
from settings import HEADER, DOMAIN, CLIENT_IDENTIFIER, logger


class Parser():

    def __init__(self):
        self.header = HEADER
        self.session = tls_client.Session(client_identifier=CLIENT_IDENTIFIER)
        self.logger = logger


    def parser(self,pdp_url):

        product_url = urljoin(DOMAIN,pdp_url)

        
        product_response = self.session.get(product_url,headers=self.header)
        self.logger.info(f"STATUS CODE = {product_response.status_code}")

        html = product_response.text


        selector = pq.Selector(text=html)

        #Product url fetch
        prod_url = product_response.url
        if product_response.status_code == 200:
            self.logger.info("Start fetching data........................")

        try:
            #product breadcrumbs fetch
            breadcrumbs_fetched = selector.xpath('//ol[@class="b43307 ea1998"]//text()').getall()
            breadcrumbs = "".join(breadcrumbs_fetched)

            #product title fetch

            Title = selector.xpath('//h1[@class="b9e19c c779b4 b44f77"]//text()').get()

            #product selling price and regular price fetch and clean logic

            selling_price = ""
            regular_price = ""
            selling_price_fetched = selector.xpath('//span[@data-testid="red-price"]//text()').get()
            if selling_price_fetched:
                regular_price_fetched = selector.xpath('//span[@data-testid="line-through-white-price"]//text()').get()
                regular_price = float(re.search(r"\d[\d,]*\.?\d*", regular_price_fetched).group().replace(",", ""))

                selling_price = float(re.search(r"\d[\d,]*\.?\d*", selling_price_fetched).group().replace(",", ""))
            else:
                regular_price_fetched = selector.xpath('//span[@data-testid="white-price"]//text()').get()

                regular_price = float(re.search(r"\d[\d,]*\.?\d*", regular_price_fetched).group().replace(",", ""))

                selling_price = regular_price


            #Description fetch

            Description = "" 
            Description_fetched = selector.xpath('//p[@class="fdb3e1 cfeb83 b493f8"]//text()').get()
            if Description_fetched:
                Description = Description_fetched
            

            #Net quantity fetch

            Net_quantity = ""
            Net_quantity_fetched = selector.xpath('//dd[@data-testid="description-netQuantityAccordions"]/text()').get()
            if Net_quantity_fetched:
                Net_quantity = Net_quantity_fetched


            # FIT fetch

            Fit = ""
            fit_fetched = selector.xpath('//dd[@data-testid="description-fits"]/text()').get()
            if fit_fetched:
                Fit = fit_fetched

            #country of origin fetch

            country_of_origin_fetched = selector.xpath('//dd[@data-testid="description-countryOfProduction"]//text()').get()
            if country_of_origin_fetched:
                Country_of_origin = country_of_origin_fetched
            else:
                Country_of_origin = ""    
            
            #diamentions fetched and cleaning and parsing logic

            diamentions_fetched = selector.xpath('//dd[@class="fdb3e1 cfeb83 f1bad1 acddb1"]//text()').getall()
            if diamentions_fetched:
                converted_string = " ".join(diamentions_fetched)
                pattern = re.findall(r'Width:\s*([\d\.]+\s*(?:cm|m))\s*,\s*Length:\s*([\d\.]+\s*(?:cm|m))',converted_string)

                Diamentions = []
                for width, length in pattern:
                    Diamentions.append({
                        "width": width,
                        "length": length
                    })
            else:
                Diamentions = ""
            
            # Fabric composition fetch, clean and logic
            
            fabric_composition_fetched = selector.xpath('//li[@class="b819ff"]//text()').getall()
            if fabric_composition_fetched:
                Fabric_composition = {}
                current = None
                for i in fabric_composition_fetched:
                    if i.endswith(":"):
                        current = i.replace(":","")
                        Fabric_composition[current] = {}
                        continue

                    parts = re.findall(r"([A-Za-z ]+)\s+(\d+%)", i)
                    parsed = {name.strip(): percent for name, percent in parts}

                    if current is None:
                        Fabric_composition.update(parsed)
                    else:
                        Fabric_composition[current].update(parsed)
            else:
                Fabric_composition = ""

            # Care instruction fetch and clean

            care_instructions_fetched = selector.xpath('//ul[@class="e00dc3"]//text()').getall()

            if care_instructions_fetched:
                Care_instructions = ",".join(care_instructions_fetched)
            else:
                Care_instructions = ""

            # model fit fetch

            model_fit_fetched = selector.xpath('//dd[@data-testid="description-modelHeightGarmentSize"]//text()').get()

            if model_fit_fetched:
                Model_fit = model_fit_fetched
            else:
                Model_fit = ""


        except Exception as e:
            self.logger.error(f"Cookie expire or {e}")


            

        

        # returning all the fetched details

        return {

            "Url": prod_url, 
            "Breadcrumbs": breadcrumbs,
            "Brand": "H&M",
            "title": Title,
            "Regular_price": regular_price,
            "Selling_price": selling_price,
            "SKU": "N/A",
            "Description": Description,
            "Diamentions" : Diamentions,
            "Net_Quantity": Net_quantity,
            "Fit": Fit,
            "Care_instructions": Care_instructions,
            "Fabric_composition": Fabric_composition,
            "Model_fit": Model_fit,
            "Country_of_origin" : Country_of_origin,



        }