from bson import ObjectId
from flask_mongoengine.json import MongoEngineJSONEncoder


class MongoEngineObjectIdJSONEncoder(MongoEngineJSONEncoder):
    """
    A JSONEncoder which provides serialization of MongoEngine
    documents and queryset objects.
    """

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return MongoEngineJSONEncoder.default(self, obj)
