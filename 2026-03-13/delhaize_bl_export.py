
import csv
import logging
from time import sleep
from settings import MONGO_COLLECTION_DATA, FILE_NAME, FILE_HEADER
from datetime import datetime, timedelta
import re

class Export:
    """Post-Processing"""

    def __init__(self,writer):
        self.writer = writer

    def start(self):
        """Export as CSV file"""
        def format_price(value):
            try:
                return f"{float(value):.2f}"
            except (TypeError, ValueError):
                return ""
            
        def format_date(value):
            date_obj = datetime.strptime(value, "%d/%m/%y")
            next_date = date_obj + timedelta(days=1)

            return next_date.strftime("%d/%m/%Y")

        self.writer.writerow(FILE_HEADER)
        logging.info(FILE_HEADER)

        for item in MONGO_COLLECTION_DATA.find(no_cursor_timeout=True).limit(200):
            unique_id = item.get("unique_id", "")
            product_unique_key = item.get("product_unique_key", "")
            competitor_product_key = item.get("competitor_product_key", "")

            product_name = item.get("product_name", "")
            brand = item.get("brand", "")
            pdp_url = item.get("pdp_url", "")
            competitor_name = item.get("competitor_name", "")
            extraction_date = item.get("extraction_date","").replace("-","_")

            regular_price = format_price(item.get("regular_price", "").strip(""))
            selling_price = format_price(item.get("selling_price", "").strip(""))

            price_per_unit_fetch = item.get("price_per_unit","")
            price_per_unit = re.search(r"\d+,\d+", price_per_unit_fetch).group().replace(",", ".") if price_per_unit_fetch else ""


           




            promotion_description_fetch = item.get("promotion_description","").strip() 
            promotion_description = promotion_description_fetch if promotion_description_fetch else ""
            
            promotion_startdate_fetch = item.get("promotion_start_date","")
            promotion_start_date = promotion_startdate_fetch if promotion_startdate_fetch else ""

            promotion_enddate_fetch = item.get("promotion_end_date","")
            promotion_end_date = format_date(promotion_enddate_fetch) if promotion_enddate_fetch else ""

            currency = "EUR"

            grammage_quantity = item.get("grammage_quantity", "")
            grammage_unit = item.get("grammage_unit", "")
            site_shown_uom = item.get("site_shown_uom", "")
            net_content = item.get("net_content")

            producthierarchy_level1 = item.get("producthierarchy_level1", "")
            producthierarchy_level2 = item.get("producthierarchy_level2", "")
            producthierarchy_level3 = item.get("producthierarchy_level3", "")
            producthierarchy_level4 = item.get("producthierarchy_level4", "")
            producthierarchy_level5 = item.get("producthierarchy_level5", "")
            producthierarchy_level6 = item.get("producthierarchy_level6", "")
            
            breadcrumb_fetch = item.get("breadcrumb", "")
            breadcrumb = " > ".join(breadcrumb_fetch) if breadcrumb_fetch else ""

            product_description = item.get("product_description", "")


            storage_instructions= item.get("storage_instructions", "")


            instructionforuse_fetch = item.get("instruction_for_use", "")
            instructionforuse = instructionforuse_fetch.strip() if instructionforuse_fetch else ""




            nutritional_information_fetch= item.get("nutritional_information", "")
            # nutritional_information = {
            #     item["id"]: item["valueList"][0]["value"]
            #     for item in nutritional_information_fetch
            # } if nutritional_information_fetch else {}
            nutritional_information = {
                item["id"]: [v["value"] for v in item["valueList"]]
                for item in nutritional_information_fetch
            } if nutritional_information_fetch else ""





            ingredients = item.get("ingredients","")

            manufacturer_address = item.get("manufacturer_details", "").replace("\n"," ")
        

            allergens = ""
            allergens_fetch = item.get("allergens",[])
            if allergens_fetch:
                for allerg in allergens_fetch:
                    if allerg.get("id") == "contain":
                        values = allerg.get("values")
                        if isinstance(values,list):
                            allergens = ", ".join(values)
                        else:
                            allergens = values
        
            special_information_fetch = item.get("special_information","")
            special_information = special_information_fetch.replace("*","").strip() if special_information_fetch else ""

            instock = item.get("instock", "")

            image = item.get("image_url", [])
            image_url_1 = image[0] if len(image) > 0 else ""
            image_url_2 = image[1] if len(image) > 1 else ""
            image_url_3 = image[2] if len(image) > 2 else ""
            image_url_4 = image[3] if len(image) > 3 else ""
            image_url_5 = image[4] if len(image) > 4 else ""
            image_url_6 = image[5] if len(image) > 5 else ""

            data = [
                unique_id,                    # unique_id
                competitor_name,               # competitor_name
                "",                            # store_name
                "",                            # store_addressline1
                "",                            # store_addressline2
                "",                            # store_suburb
                "",                            # store_state
                "",                            # store_postcode
                "",                            # store_addressid
                extraction_date,               # extraction_date
                product_name,                  # product_name
                brand,                         # brand
                "",                            # brand_type
                grammage_quantity,             # grammage_quantity
                grammage_unit,                 # grammage_unit
                "",                            # drained_weight
                producthierarchy_level1,       # producthierarchy_level1
                producthierarchy_level2,       # producthierarchy_level2
                producthierarchy_level3,       # producthierarchy_level3
                producthierarchy_level4,       # producthierarchy_level4
                producthierarchy_level5,             # producthierarchy_level5
                producthierarchy_level6,                # producthierarchy_level6
                "",                            # producthierarchy_level7
                regular_price,                 # regular_price
                selling_price,                 # selling_price
                "",                            # price_was
                "",               # promotion_price
                promotion_start_date,                            # promotion_valid_from
                promotion_end_date,                            # promotion_valid_upto
                "",                            # promotion_type
                "",           # percentage_discount
                promotion_description,         # promotion_description
                "",                            # package_sizeof_sellingprice
                "",                            # per_unit_sizedescription
                "",                            # price_valid_from
                price_per_unit,                            # price_per_unit
                "",                            # multi_buy_item_count
                "",                            # multi_buy_items_price_total
                currency,                      # currency
                breadcrumb,                    # breadcrumb
                pdp_url,                       # pdp_url
                "",                            # variants
                product_description,           # product_description
                "",                            # instructions
                storage_instructions,          # storage_instructions
                "",                            # preparationinstructions
                instructionforuse,             # instructionforuse
                "",             # country_of_origin
                allergens,                            # allergens
                "",                            # age_of_the_product
                "",                            # age_recommendations
                "",                            # flavour
                "",                            # nutritions
                nutritional_information,       # nutritional_information
                "",                            # vitamins
                "",                            # labelling
                "",                            # grade
                "",                            # region
                "",                            # packaging
                "",                            # receipies
                "",                            # processed_food
                "",                            # barcode
                "",                            # frozen
                "",                            # chilled
                "",                            # organictype
                "",                            # cooking_part
                "",                            # Handmade
                "",                            # max_heating_temperature
                special_information,                            # special_information
                "",                            # label_information
                "",                            # dimensions
                "",                            # special_nutrition_purpose
                "",                            # feeding_recommendation
                "",                            # warranty
                "",                            # color
                "",                            # model_number
                "",                            # material
                "",                            # usp
                "",                            # dosage_recommendation
                "",                            # tasting_note
                "",                            # food_preservation
                "",                            # size
                "",                        # rating
                "",                        # review
                "",                            # file_name_1
                image_url_1,                   # image_url_1
                "",                            # file_name_2
                image_url_2,                   # image_url_2
                "",                            # file_name_3
                image_url_3,                   # image_url_3
                "",                            # file_name_4
                image_url_4,                   # image_url_4
                "",                            # file_name_5
                image_url_5,                   # image_url_5
                "",                            # file_name_6
                image_url_6,                   # image_url_6
                competitor_product_key,        # competitor_product_key
                "",                            # fit_guide
                "",                            # occasion
                "",                            # material_composition
                "",                            # style
                "",                            # care_instructions
                "",                            # heel_type
                "",                            # heel_height
                "",                            # upc
                "",                      # features
                "",                            # dietary_lifestyle
                manufacturer_address,          # manufacturer_address
                "",                            # importer_address
                "",                            # distributor_address
                "",                            # vinification_details
                "",                            # recycling_information
                "",                            # return_address
                "",                            # alchol_by_volume
                "",                            # beer_deg
                net_content,                            # netcontent
                "",                            # netweight
                site_shown_uom,                # site_shown_uom
                ingredients,                   # ingredients
                "",                            # random_weight_flag
                instock,                       # instock
                "",                            # promo_limit
                product_unique_key,            # product_unique_key
                "",                            # multibuy_items_pricesingle
                "",                            # perfect_match
                "",                            # servings_per_pack
                "",                            # Warning
                "",                            # suitable_for
                "",                            # standard_drinks
                "",                            # environmental
                "",                            # grape_variety
                ""                             # retail_limit
            ]

            self.writer.writerow(data)


if __name__ == "__main__":
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        writer_file = csv.writer(file, delimiter="|", quotechar='"')
        export = Export(writer_file)
        export.start()
        file.close()

# class Export:
#     """Post-Processing CSV Export"""

#     def __init__(self, writer):
#         self.writer = writer

#     def start(self):
#         def format_price(value):
#             try:
#                 return f"{float(value):.2f}"
#             except (TypeError, ValueError):
#                 return ""
#         # write header
#         self.writer.writerow(FILE_HEADERS)
#         logging.info("CSV headers written")

#         for item in MONGO_COLLECTION_DATA.find(no_cursor_timeout=True):
            
#             row = [
#                 item.get("unique_id", ""),
#                 item.get("product_unique_key", ""),
#                 item.get("competitor_product_key", ""),
#                 item.get("product_name", ""),
#                 item.get("brand", ""),
#                 item.get("pdp_url", ""),
#                 item.get("competitor_name", ""),
#                 item.get("extraction_date", ""),
#                 item.get("regular_price", ""),
#                 item.get("selling_price", ""),
#                 item.get("price_was", ""),
#                 item.get("percentage_discount", ""),
#                 item.get("currency", ""),
#                 item.get("grammage_quantity", ""),
#                 item.get("grammage_unit", ""),
#                 item.get("site_shown_uom", ""),
#                 item.get("producthierarchy_level1", ""),
#                 item.get("producthierarchy_level2", ""),
#                 item.get("producthierarchy_level3", ""),
#                 item.get("producthierarchy_level4", ""),
#                 item.get("breadcrumb", ""),
#                 item.get("product_description", ""),
#                 item.get("storage_instructions", ""),
#                 item.get("instructionforuse", ""),
#                 item.get("nutritional_information", ""),
#                 item.get("country_of_origin", ""),
#                 item.get("ingredients", ""),
#                 item.get("manufacturer_address", ""),
#                 item.get("features", ""),
#                 item.get("rating", ""),
#                 item.get("review", ""),
#                 item.get("instock", ""),
#                 item.get("image_url_1", ""),
#                 item.get("image_url_2", ""),
#                 item.get("image_url_3", ""),
#                 item.get("image_url_4", ""),
#                 item.get("image_url_5", ""),
#                 item.get("image_url_6", ""),
#             ]

#             self.writer.writerow(row)

        # logging.info("CSV export completed successfully")

# if __name__ == "__main__":
#     with open(FILE_NAME, "w", encoding="utf-8", newline="") as file:
#         writer_file = csv.writer(
#             file,
#             delimiter="|",          # PIPE delimiter
#             quotechar='"',
#             quoting=csv.QUOTE_MINIMAL
#         )

#         export = Export(writer_file)
#         export.start()

