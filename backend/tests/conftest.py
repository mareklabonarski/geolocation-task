import json
import os
from unittest.mock import create_autospec

import pytest
import requests
from mongoengine import disconnect
from requests import Response, RequestException

from backend import models
from backend.api.endpoints.geoip import IPSTACK_URL
from backend.app import create_app


FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


fixtures_mapping = {
    'www.youtube.com': 'youtube.json',
    'www.wp.pl': 'wp.json',
}


def ipstack_mock_response_content(url):
    ip_or_url = url.split(IPSTACK_URL)[-1]
    for host, file in fixtures_mapping.items():
        with open(os.path.join(FIXTURES_PATH, file)) as f:
            content = json.load(f)
            if ip_or_url == host:
                return content
            for elem in content:
                if elem['ip'] == ip_or_url:
                    return [elem]


@pytest.fixture
def mock_get_ips_for_host(mocker):
    def _get_ips_for_host(url):
        ips = set()
        for host, file in fixtures_mapping.items():
            if host in url:
                with open(os.path.join(FIXTURES_PATH, file)) as f:
                    content = json.load(f)
                for elem in content:
                    ips.add(elem['ip'])
                break
        return ips
    yield mocker.patch('backend.api.endpoints.geoip.get_ips_for_host', new=_get_ips_for_host)


@pytest.fixture
def mock_ipstack(mocker):
    def get_response(url, *args, **kwargs):
        if IPSTACK_URL in url:
            response = create_autospec(Response)
            response.json = lambda: ipstack_mock_response_content(url)[0]
            return response

        return requests.get(url, *args, **kwargs)

    yield mocker.patch.object(requests, 'get', new=get_response)


@pytest.fixture
def mock_ipstack_unavailable(mocker):
    def get_response(url, *args, **kwargs):
        if IPSTACK_URL in url:
            raise RequestException
        return requests.get(url, *args, **kwargs)

    yield mocker.patch.object(requests, 'get', new=get_response)


@pytest.fixture
def clean_db():
    _models = ['GeoIP']
    for model in _models:
        getattr(models, model).drop_collection()


@pytest.fixture
def test_app():
    app = create_app(mock_db=True)
    yield app
    disconnect()


@pytest.fixture
def test_app_no_db_mock():
    app = create_app(mock_db=False)
    yield app
    disconnect()


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def client_no_db_mock(test_app_no_db_mock):
    with test_app_no_db_mock.test_client() as client:
        yield client
