import hashlib

from flask_mongoengine import DynamicDocument, Document
from mongoengine import fields, NotUniqueError


def to_md5(password):
    return hashlib.md5(password.encode()).hexdigest()


def add_sofomo_user():
    try:
        User.create_user(username='sofomo', password='sofomo').save()
    except NotUniqueError:
        pass


class GeoIP(DynamicDocument):
    ip = fields.StringField(primary_key=True)


class User(Document):
    username = fields.StringField(primary_key=True)
    password = fields.StringField()

    @property
    def id(self):
        return self.username

    @classmethod
    def create_user(cls, username, password):
        return cls(username=username, password=to_md5(password))
