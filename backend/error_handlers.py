from flask_jwt import JWTError
from pymongo.errors import PyMongoError

from backend.api import api
from backend.api.endpoints.geoip import HostResolutionError
from backend.auth import jwt


def service_temporarily_unavailable():
    return {'message': 'Service temporarily unavailable'}, 503


def handle_jwt_error(error):
    return {'description': error.description, 'error': error.error}, error.status_code


def add_error_handlers(flask_app):

    @api.errorhandler(JWTError)
    def handle_unauthorized_error(error):  # strange that this was needed and didn't come automatically
        return handle_jwt_error(error)

    @jwt.jwt_error_handler
    @api.errorhandler(PyMongoError)
    @api.errorhandler(HostResolutionError)
    @flask_app.errorhandler(PyMongoError)
    @flask_app.errorhandler(HostResolutionError)
    def handle_service_error(error):
        if isinstance(error, JWTError):
            return handle_jwt_error(error)

        return service_temporarily_unavailable()
