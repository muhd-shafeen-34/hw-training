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

    
    