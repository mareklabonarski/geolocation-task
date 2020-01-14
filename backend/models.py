from flask_mongoengine import DynamicDocument
from mongoengine import fields


class GeoIP(DynamicDocument):
    ip = fields.StringField(primary_key=True)
