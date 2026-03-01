from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField

class ProductItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    url = StringField()
    product_name = StringField()
    brand = StringField()
    currency = StringField()
    review_dict_list = ListField()


class ProductUrlItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    unique_id = StringField(required=True,unique=True)
    pdp_url = StringField(required=True,unique=True)
    name = StringField()
    grammage_details = StringField()
    regular_price = StringField()
    selling_price = StringField()
    discount = StringField()
    brand = StringField()
    ean_code = StringField()
    rating = StringField()
    review = StringField()
    images = ListField()


class Product(DynamicDocument):
    meta = {"db_alias": "default"}

    # Core identifiers
    unique_id = StringField(required=True, unique=True)
    product_unique_key = StringField()
    competitor_product_key = StringField()  # ean code

    # Basic product info
    product_name = StringField()
    brand = StringField()
    pdp_url = StringField(required=True, unique=True)
    competitor_name = StringField()
    extraction_date = StringField()

    # Pricing
    regular_price = StringField()
    selling_price = StringField()
    price_was = StringField()
    percentage_discount = StringField()
    currency = StringField()

    # Grammage
    grammage_quantity = StringField()
    grammage_unit = StringField()
    site_shown_uom = StringField()

    # Hierarchy / breadcrumb
    producthierarchy_level1 = StringField()
    producthierarchy_level2 = StringField()
    producthierarchy_level3 = StringField()
    producthierarchy_level4 = StringField()
    breadcrumb = StringField()

    # Content
    product_description = StringField()
    storage_instructions = StringField()
    instructionforuse = StringField()
    nutritional_information = StringField()
    country_of_origin = StringField()
    ingredients = StringField()
    manufacturer_address = StringField()
    features = StringField()

    # Reviews / rating
    rating = StringField()
    review = StringField()
    instock = BooleanField()

    # Images
    image_url_1 = StringField()
    image_url_2 = StringField()
    image_url_3 = StringField()
    image_url_4 = StringField()
    image_url_5 = StringField()
    image_url_6 = StringField()






class ProductCatUrlItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    url = StringField(required=True)
    name = StringField()
    slug = StringField()
    type = StringField()
    
    

