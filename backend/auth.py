from flask_jwt import JWT
from mongoengine import DoesNotExist

from backend.models import User, to_md5


def authenticate(username, password):
    try:
        return User.objects.get(username=username, password=to_md5(password))
    except DoesNotExist:
        return None


def identity(payload):
    username = payload['identity']
    return User.objects.get(username=username)


jwt = JWT(None, authenticate, identity)
