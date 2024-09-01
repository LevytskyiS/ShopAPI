from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, IntField


class NomenclatureMongo(Document):
    code = StringField(max_length=7, required=True)
    quantity = IntField(required=True)
    stock = DateTimeField(required=True)


class UserMongo(Document):
    tg_id = IntField(required=True)
    name = StringField(required=True)
