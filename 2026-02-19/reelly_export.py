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
            name = item.get("name")
            price = item.get("price")
            image_url= item.get("image_url")
            status = item.get("status")
            developer = item.get("developer")
            unit_types = item.get("unit_types")
            district = item.get("district")
            description = item.get("description")
            data = [
                unique_id,
                url,
                name,
                price,
                image_url,
                status,
                developer,
                unit_types,
                district,
                description,

            ]

            self.writer.writerow(data)


if __name__ == "__main__":
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        writer_file = csv.writer(file, delimiter=",", quotechar='"')
        export = Export(writer_file)
        export.start()
        file.close()