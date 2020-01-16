import os

from flask import Flask, Blueprint
from flask_mongoengine import MongoEngine

from backend.api import api
from backend.api.endpoints.geoip import geo_ns
from backend.auth import jwt
from backend.encoder import MongoEngineObjectIdJSONEncoder
from backend.error_handlers import add_error_handlers
from backend.models import add_sofomo_user


def create_app(mock_db=False):
    app = Flask(__name__)
    initialize_app(app, mock_db=mock_db)
    return app


def get_config(mock_db=False):

    config = {
        'RESTPLUS_JSON': {'cls': MongoEngineObjectIdJSONEncoder},
        'MONGODB_SETTINGS': {
            'host': 'mongodb://db:27017/sofomo' if not mock_db else 'mongomock://localhost:27017',
            'connect': True,
        }
    }
    return config


def configure_app(flask_app, mock_db=False):
    flask_app.config.from_mapping(get_config(mock_db=mock_db))

    flask_app.config.update(
        JWT=jwt,
        JWT_SECRET_KEY='jwt-secret'
    )


def initialize_app(flask_app, mock_db=False):
    configure_app(flask_app, mock_db=mock_db)

    jwt.init_app(flask_app)
    MongoEngine(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(geo_ns)
    flask_app.register_blueprint(blueprint)

    add_error_handlers(flask_app)

    if os.getenv('ADD_SOFOMO_USER', False):
        add_sofomo_user()


def main():
    app = create_app()
    app.run(debug=os.getenv('DEBUG', True))


if __name__ == '__main__':
    main()
