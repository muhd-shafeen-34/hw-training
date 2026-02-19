from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField
import settings

class ProductUrl(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    unique_id = StringField(unique=True)
    url = StringField(unique=True)
    api_url = StringField(unique=True)
    name = StringField()


class ProductItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default"}
    unique_id = StringField(unique=True)
    url = StringField(unique=True)
    name = StringField()
    price = StringField()
    image_url = StringField()
    status = StringField()
    developer = StringField()
    unit_types = StringField()
    district = StringField()
    description = StringField()
