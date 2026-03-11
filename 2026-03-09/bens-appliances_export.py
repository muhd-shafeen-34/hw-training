import csv
import logging
from time import sleep
from settings import MONGO_COLLECTION_DATA, FILE_NAME, FILE_HEADER

import re

class Export:
    """Post-Processing"""

    def __init__(self,writer):
        self.writer = writer

    def start(self):
        """Export as CSV file"""
        def format_price(value):
            try:
                number = re.search(r'\d+(?:\.\d+)?', str(value))
                return f"{float(number.group()):.2f}" if number else ""
            except (TypeError, ValueError):
                return ""

        self.writer.writerow(FILE_HEADER)
        logging.info(FILE_HEADER)

        

        for item in MONGO_COLLECTION_DATA.find(no_cursor_timeout=True):

            input_part_number = item.get("input_part_no")
            url = item.get("url")
            title = item.get("title")
            manufacturer = item.get("manufacturer")
            price_fetch = item.get("price")

            price = format_price(price_fetch)

            description_fetch= item.get("description")
            desc_clean = re.sub(r'[\ufeff\xa0]|<!--.*?-->|<[^>]+>|\s+', ' ', description_fetch).strip()
            description = desc_clean if desc_clean else description_fetch


            availability = item.get("availability")
            image_urls = item.get("image_urls")
            compatible_products_fetch = item.get("compatible_product")
            if input_part_number in compatible_products_fetch:
                compatible_products_fetch.remove(input_part_number)
            if "1000" in compatible_products_fetch:
                compatible_products_fetch.remove("1000")
            compatible_products = ", ".join(compatible_products_fetch)
            equivalent_part_numbers_fetch = item.get("equivalent_par_numbers")
            if input_part_number in equivalent_part_numbers_fetch:
                equivalent_part_numbers_fetch.remove(input_part_number)
            if "120V" in equivalent_part_numbers_fetch:
                equivalent_part_numbers_fetch.remove("120V")
            
            if "2600" in equivalent_part_numbers_fetch:
                equivalent_part_numbers_fetch.remove("2600")
            
            equivalent_part_numbers = ", ".join(equivalent_part_numbers_fetch)


            data = [
                input_part_number,
                url,
                title,
                manufacturer,
                price,
                description,
                "",
                "",
                "",
                compatible_products,
                equivalent_part_numbers,
                "",
                "",
                availability,
                image_urls,
                "",





            ]

            self.writer.writerow(data)


if __name__ == "__main__":
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        writer_file = csv.writer(file, delimiter=",", quotechar='"')
        export = Export(writer_file)
        export.start()
        file.close()