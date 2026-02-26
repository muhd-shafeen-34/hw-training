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
    brand = StringField()
    ean_code = StringField()
    images = ListField()







class ProductCatUrlItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    url = StringField(required=True)
    name = StringField()
    slug = StringField()
    type = StringField()
    
    

