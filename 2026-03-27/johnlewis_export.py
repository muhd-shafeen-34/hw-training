
import csv
import logging
from time import sleep
from settings import MONGO_COLLECTION_DATA, FILE_NAME, FILE_HEADER
from datetime import datetime, timedelta
import re
import json

class Export:
    """Post-Processing"""

    def __init__(self,writer):
        self.writer = writer

    def start(self):
        """Export as CSV file"""
        def clean_text(value):
            if isinstance(value, str):
                # remove patterns like <0x81>
                value = re.sub(r'<0x[0-9A-Fa-f]+>', '', value)

                # remove non-printable / weird chars
                value = re.sub(r'[^\x20-\x7E]+', ' ', value)

                # normalize spaces
                value = re.sub(r'\s+', ' ', value).strip()
            return value


        def clean_dict(data):
            if isinstance(data, dict):
                return {clean_text(k): clean_dict(v) for k, v in data.items()}

            elif isinstance(data, list):
                return [clean_dict(i) for i in data]

            else:
                return clean_text(data)
    

        def format_price(value):
            try:
                return f"{float(value):.2f}"
            except (TypeError, ValueError):
                return ""

        self.writer.writerow(FILE_HEADER)
        logging.info(FILE_HEADER)

        for item in MONGO_COLLECTION_DATA.find(no_cursor_timeout=True).limit(200):
            unique_id = item.get("unique_id", "")
            product_unique_key = f"{unique_id}P"

            product_name_fetch = item.get("product_name", "")
            product_name = product_name_fetch if product_name_fetch else ""
            brand = item.get("brand", "")
            pdp_url = item.get("pdp_url", "")
            competitor_name = "johnlewis"
            extraction_date = item.get("extraction_date","")
            
            regular_price_fetch = item.get("regular_price", "")
            regular_price_text = regular_price_fetch if regular_price_fetch else ""

            selling_price_fetch = item.get("selling_price", "")
            selling_price_text = selling_price_fetch if selling_price_fetch else ""

            regular_price = format_price(regular_price_text).strip("")
            selling_price = format_price(selling_price_text).strip("")
           
            if regular_price == selling_price:
                price_was = ""
            else:
                price_was = regular_price



            currency = "GBP"

            breadcrumb_list = item.get("breadcrumb_list","")
            breadcrumb = " > ".join(breadcrumb_list)
            producthierarchy_level1 = breadcrumb_list[0] if len(breadcrumb_list) > 0 else ""
            producthierarchy_level2 = breadcrumb_list[1] if len(breadcrumb_list) > 1 else ""
            producthierarchy_level3 = breadcrumb_list[2] if len(breadcrumb_list) > 2 else ""
            producthierarchy_level4 = breadcrumb_list[3] if len(breadcrumb_list) > 3 else ""
            producthierarchy_level5 = breadcrumb_list[4] if len(breadcrumb_list) > 4 else ""
            producthierarchy_level6 = breadcrumb_list[5] if len(breadcrumb_list) > 5 else ""

            pdp_url = item.get("pdp_url","")
            
            promotion_description_fetch = item.get("promotion_description","").strip() 
            promotion_description = promotion_description_fetch if promotion_description_fetch else ""

            discount_regex = re.search(r"%\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*%", promotion_description)
            percentage_discount = discount_regex.group(1) if discount_regex else ""
    

            product_description_fetch = item.get("product_description", "")
            product_description_text = re.sub(r'\s+', ' ', product_description_fetch).strip() if product_description_fetch else ""

            product_description = product_description_text if product_description_text else ""

            instock = item.get("instock", "")
            
            image = item.get("images",[])
            image_url_1 = f"https:{image[0]}" if len(image) > 0 else ""
            image_url_2 = f"https:{image[1]}" if len(image) > 1 else ""
            image_url_3 = f"https:{image[2]}" if len(image) > 2 else ""
            image_url_4 = f"https:{image[3]}" if len(image) > 3 else ""
            image_url_5 = f"https:{image[4]}" if len(image) > 4 else ""
            image_url_6 = f"https:{image[5]}" if len(image) > 5 else ""

            color = item.get("color","")
            size = item.get("size","")
            rating = item.get("rating","")
            if rating == "0":
                rating = ""
            review = item.get("review","")
            if review == "0":
                review = ""
                

            var_attributes = item.get("attributes",[])
            page_attribute = item.get("pageinfo",[])
            country_of_origin_fetch = ""
            material_composition_fetch = ""
            care_instruction_fetch = []
            fit_guide_fetch = ""

            for details in var_attributes:
                if details.get("key","") == "countryoforigin":
                
                    country_of_origin_fetch = details.get("values",[])
                if details.get("key","") == "material":
                    material_composition_fetch = details.get("values",[])
                if details.get("key","") == "washinginstructionsnew":
                    
                    care_instruction_fetch.append(details.get("values",[]))

            for details in page_attribute:
                if details.get("key","") == "careinstructions":
                    care_instruction_fetch.append(details.get("values",[]))
                if details.get("key","") == "jeantrousercut":
                    fit_guide_fetch = details.get("values",[])

            country_of_origin = "".join(country_of_origin_fetch) if country_of_origin_fetch else ""
            care_instruction = ",".join(i[0] for i in care_instruction_fetch) if care_instruction_fetch else ""
            fit_guide = "".join(fit_guide_fetch) if fit_guide_fetch else ""
            material_composition_fetch = "".join(material_composition_fetch) if material_composition_fetch else ""

            material_composition = re.sub(r'\s+', ' ', material_composition_fetch).strip() if material_composition_fetch else ""


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
                "",             # grammage_quantity
                "",                 # grammage_unit
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
                price_was,                            # price_was
                "",               # promotion_price
                "",                            # promotion_valid_from
                "",                            # promotion_valid_upto
                "",                            # promotion_type
                percentage_discount,           # percentage_discount
                promotion_description,         # promotion_description
                "",                            # package_sizeof_sellingprice
                "",                            # per_unit_sizedescription
                "",                            # price_valid_from
                "",                            # price_per_unit
                "",                            # multi_buy_item_count
                "",                            # multi_buy_items_price_total
                currency,                      # currency
                breadcrumb,                    # breadcrumb
                pdp_url,                       # pdp_url
                "",                            # variants
                product_description,           # product_description
                "",                            # instructions
                "",          # storage_instructions
                "",                            # preparationinstructions
                "",             # instructionforuse
                country_of_origin,             # country_of_origin
                "",                            # allergens
                "",                            # age_of_the_product
                "",                            # age_recommendations
                "",                            # flavour
                "",                            # nutritions
                "",       # nutritional_information
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
                "",                            # special_information
                "",                            # label_information
                "",                            # dimensions
                "",                            # special_nutrition_purpose
                "",                            # feeding_recommendation
                "",                            # warranty
                color,                            # color
                "",                            # model_number
                "",                            # material
                "",                            # usp
                "",                            # dosage_recommendation
                "",                            # tasting_note
                "",                            # food_preservation
                size,                            # size
                rating,                        # rating
                review,                        # review
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
                "",        # competitor_product_key
                fit_guide,                            # fit_guide
                "",                            # occasion
                material_composition,                            # material_composition
                "",                            # style
                care_instruction,                            # care_instructions
                "",                            # heel_type
                "",                            # heel_height
                "",                            # upc
                "",                      # features
                "",                            # dietary_lifestyle
                "",          # manufacturer_address
                "",                            # importer_address
                "",                            # distributor_address
                "",                            # vinification_details
                "",                            # recycling_information
                "",                            # return_address
                "",                            # alchol_by_volume
                "",                            # beer_deg
                "",                            # netcontent
                "",                            # netweight
                "",                # site_shown_uom
                "",                   # ingredients
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