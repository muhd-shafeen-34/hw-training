from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField


class ProductUrls(DynamicDocument):
    meta = {"db_alias": "default"}
    pdp_url = StringField()
    rating = StringField()
    review = StringField()
    brand = StringField()
    attributes = ListField()



class ProductItems(DynamicDocument):
        unique_id = StringField()
        extraction_date = StringField()
        product_name = StringField()
        brand = StringField()
        regular_price = StringField()
        selling_price = StringField()
        promotion_description = StringField()
        breadcrumb_list = ListField()
        pdp_url = StringField()
        product_description = StringField()
        color = StringField()
        item = StringField()
        reviews = StringField()
        image_list = ListField()
        attributes =ListField()
        instock = BooleanField()
        pageinfo = ListField()
        
