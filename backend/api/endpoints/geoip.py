import os
import re
import socket

import requests
from flask import request
from flask_jwt import jwt_required
from flask_restplus import Resource, abort
from mongoengine import DoesNotExist
from requests import RequestException

from backend.api import api
from backend.models import GeoIP


IPSTACK_URL = 'http://api.ipstack.com/'
GEO_IP_KEY = os.getenv('GEO_IP_KEY')

geo_ns = api.namespace('geoip')


class HostResolutionError(Exception):
    pass


def get_ips_for_host(url):
    url = re.split(r'https?://', url)[-1]
    url = url.split('/')[0]
    ips = set()
    try:
        for info in socket.getaddrinfo(url, None):
            *_, (ip, *_) = info
            ips.add(ip)
    except OSError as e:
        raise HostResolutionError from e
    return ips


class AuthResource(Resource):
    method_decorators = [jwt_required()]
    pass


@geo_ns.route('/ip/<string:ip>')
class GeoIPResource(AuthResource):

    def get(self, ip):
        return GeoIP.objects.get_or_404(pk=ip).to_mongo()

    def delete(self, ip):
        GeoIP.objects.get_or_404(pk=ip).delete()
        return '', 204


@geo_ns.route('/url/<string:url>')
class GeoIPURLResource(AuthResource):

    def get(self, url):
        ips = get_ips_for_host(url)
        for ip in ips:
            try:
                geoip = GeoIP.objects.get(ip=ip)
            except DoesNotExist:
                pass
            else:
                return geoip.to_mongo()

        abort(404)

    def delete(self, url):
        ips = get_ips_for_host(url)

        if not ips:
            abort(404)

        not_found = True
        for ip in ips:
            try:
                geoip = GeoIP.objects.get(ip=ip)
            except DoesNotExist:
                pass
            else:
                geoip.delete()
                not_found = False
        if not_found:
            abort(404)

        return '', 204


@geo_ns.route('/')
class GeoIPListResource(AuthResource):

    def get(self):
        # pagination would be good, but not in scope of the task
        return GeoIP.objects.all()

    def post(self):
        url = request.get_json().get('url')
        ip = request.get_json().get('ip')
        ips = []

        if not url and not ip:
            abort(400, message="Request need to contain 'url' or 'ip' parameter")

        if url:
            ips = get_ips_for_host(url)

        if ip and url and ip not in ips:
            abort(400, message="Given 'ip' parameter does not correspond to given 'url'!")

        ips = [ip] if ip else ips  # if both url and ip was provided, limit to provided ip only

        created = []
        with requests.Session() as session:
            for ip in ips:
                url = f'{IPSTACK_URL}{ip}'
                try:
                    response = session.get(url, params={'access_key': GEO_IP_KEY})
                    response.raise_for_status()
                except RequestException:
                    from backend.error_handlers import service_temporarily_unavailable

                    return service_temporarily_unavailable()
                else:
                    data = response.json()
                    print(data)

                    try:
                        GeoIP.objects.get(ip=data['ip'])
                    except DoesNotExist:
                        created.append(GeoIP.objects.create(**data).to_mongo())

        return created, 201 if created else 302
