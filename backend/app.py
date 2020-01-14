import os

from flask import Flask, Blueprint
from flask_mongoengine import MongoEngine

from backend.api import api
from backend.api.endpoints.geoip import geo_ns
from backend.encoder import MongoEngineObjectIdJSONEncoder


def create_app(mock_db=False):
    app = Flask(__name__)
    initialize_app(app, mock_db=mock_db)
    return app


def get_config(mock_db=False):

    config = {
        'RESTPLUS_JSON': {'cls': MongoEngineObjectIdJSONEncoder},
        'MONGODB_SETTINGS': {
            'host': 'mongodb://db:27017/sofomo' if not mock_db else 'mongomock://localhost:27017',
            'connect': False,
        }
    }
    return config


def configure_app(flask_app, mock_db=False):
    flask_app.config.from_mapping(get_config(mock_db=mock_db))


def initialize_app(flask_app, mock_db=False):
    configure_app(flask_app, mock_db=mock_db)

    MongoEngine(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(geo_ns)
    flask_app.register_blueprint(blueprint)


def main():
    app = create_app()
    app.run(debug=os.getenv('DEBUG', True))


if __name__ == '__main__':
    main()
