from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField



class ProductUrls(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}

    pdp_url = StringField(unique=True)
    pdp_name = StringField()
    pdp_price = StringField()
    pdp_manufacturer = StringField()


class ProductData(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}

    input_part_no = StringField(unique=True)
    url = StringField(unique=True)
    title = StringField()
    manufacturer = StringField()
    price = StringField()
    description = StringField()
    availability = StringField()
    image_urls = StringField()
    compatible_product = ListField()
    equivalent_par_numbers = ListField()

