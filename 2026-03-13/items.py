from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField


class ProductUrls(DynamicDocument):
    meta = {"db_alias": "default"}
    unique_id = StringField()
    name = StringField()
    brand = StringField()
    pdp_url = StringField()
    grammage_details = StringField()
    price = FloatField()
    unit_price = StringField()
    image_url = StringField()
    rating = StringField()
    review = StringField()
    promotion_description = ListField()
    promotion_startDate = ListField()
    promotion_endDate = ListField()
    instock = StringField()
    country = StringField()


class ProductItems(DynamicDocument):
    meta = {"db_alias": "default"}
    unique_id = StringField()
    competitor_name = StringField()
    extraction_date = StringField()
    brand = StringField()
    grammage_quantity = StringField()
    grammage_unit = StringField()
    product_name = StringField()
    breadcrumb = ListField()
    producthierarchy_level1 = StringField()
    producthierarchy_level2 = StringField()
    producthierarchy_level3 = StringField()
    producthierarchy_level4 = StringField()
    producthierarchy_level5 = StringField()
    producthierarchy_level6 = StringField()
    regular_price = StringField()
    selling_price = StringField()
    price_per_unit = StringField()
    currency = StringField()
    pdp_url = StringField()
    product_description = StringField()
    nutritional_information = ListField()
    ingredients = StringField()
    allergens = ListField()
    storage_instructions = StringField()
    manufacturer_details = StringField()
    net_content = StringField()
    special_information = StringField()
    instruction_for_use = StringField()
    site_shown_uom = StringField()
    competitor_product_key = StringField()
    instock = StringField()
    product_unique_key = StringField()
    image_url = ListField()
    promotion_description = ListField()
    promotion_start_date = ListField()
    promotion_end_date = ListField()

    











    





    
    