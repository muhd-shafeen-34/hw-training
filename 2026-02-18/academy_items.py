from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField
import settings

class ProductItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    unique_id = StringField(unique=True)
    url = StringField(unique=True)
    productname = StringField()
    brand = StringField()
    selling_price = StringField()
    regular_price = StringField()
    discount = StringField()
    description = StringField()
    specifications = DictField()
    image_url = StringField()
    size = StringField()
    color = StringField()
    rating = StringField()
    review = StringField()
    fit_type = StringField()
