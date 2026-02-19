import csv
import logging
from time import sleep
from settings import MONGO_COLLECTION_DATA, FILE_NAME, FILE_HEADERS



class Export:
    """Post-Processing"""

    def __init__(self,writer):
        self.writer = writer

    def start(self):
        """Export as CSV file"""

        self.writer.writerow(FILE_HEADERS)
        logging.info(FILE_HEADERS)

        for item in MONGO_COLLECTION_DATA.find(no_cursor_timeout=True):
            unique_id = item.get("unique_id")
            url = item.get("url")
            productname = item.get("productname")
            brand = item.get("brand")
            selling_price = item.get("selling_price")
            regular_price = item.get("regular_price")
            description = item.get("description")
            discount = item.get("discount")
            specification = item.get("specifications")
            size = item.get("size")
            image_url = item.get("image_url")
            color = item.get("color")
            rating = item.get("rating")
            review = item.get("review")
            fit_type = item.get("fit_type")
            data = [
                unique_id,
                url,
                productname,
                brand,
                selling_price,
                regular_price,
                discount,
                description,
                specification,
                fit_type,
                image_url,
                rating,
                review,
                size,
                color,


            ]

            self.writer.writerow(data)


if __name__ == "__main__":
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        writer_file = csv.writer(file, delimiter=",", quotechar='"')
        export = Export(writer_file)
        export.start()
        file.close()