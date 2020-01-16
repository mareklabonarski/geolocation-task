import pytest
from mongoengine import NotUniqueError
from pymongo.errors import PyMongoError

from backend.models import GeoIP, add_sofomo_user
from backend.tests.conftest import ipstack_mock_response_content


test_params = [
    ({'url': 'www.youtube.com'}),
    ({'url': 'www.wp.pl'}),
    ({'ip': '212.77.98.9'}),
    ({'ip': '2a00:1450:401b:803::200e'}),
]


def populate_db():

    for key_value in test_params:
        key, value = list(key_value.items())[0]

        content = ipstack_mock_response_content(value)
        for elem in content:
            try:
                GeoIP.objects.create(**elem)
            except NotUniqueError:
                pass
    return test_params


@pytest.mark.parametrize('endpoint', [
    '', 'ip/something', 'url/something'
])
def test_unauthorized(client, endpoint):
    response = client.get(f'/api/geoip/{endpoint}')
    assert response.status_code == 401


def request_auth(_client, username='sofomo', password='sofomo'):
    response = _client.post('/auth', json={'username': username, 'password': password})
    return response


def test_auth(client):
    response = request_auth(client)
    assert response.status_code == 401

    add_sofomo_user()

    response = request_auth(client)
    assert response.status_code == 200

    response = request_auth(client, 'not-existing')
    assert response.status_code == 401


@pytest.mark.parametrize('data', test_params)
def test_geoiplist_post(authorized_client, mock_ipstack, mock_get_ips_for_host, data):
    response = authorized_client.post('/api/geoip/', json=data)

    assert response.status_code == 201
    # 'ip' from ipstack response becomes '_id' in mongodb
    for elem in response.json:
        elem['ip'] = elem.pop('_id')
    assert all(elem in response.json for elem in ipstack_mock_response_content(list(data.values())[0]))

    response = authorized_client.post('/api/geoip/', json=data)

    assert response.status_code == 302
    for elem in response.json:
        elem['ip'] = elem.pop('_id')
    assert response.json == []


@pytest.mark.parametrize('data', test_params)
def test_geoiplist_post_ipstack_unavailable(authorized_client, mock_ipstack_unavailable, data):
    response = authorized_client.post('/api/geoip/', json=data)

    assert response.status_code == 503


def test_geoiplist_auth_db_unavailable(client, mocker, mock_ipstack, mock_get_ips_for_host):
    add_sofomo_user()
    objects_mock = mocker.patch('backend.models.User.objects')
    objects_mock.get.side_effect = PyMongoError
    objects_mock.create.side_effect = PyMongoError

    response = client.post('/auth', json={'username': 'sofomo', 'password': 'sofomo'})

    assert response.status_code == 503


@pytest.mark.parametrize('data', test_params)
def test_geoiplist_post_db_unavailable(authorized_client, mocker, mock_ipstack, mock_get_ips_for_host, data):

    objects_mock = mocker.patch('backend.models.GeoIP.objects')
    objects_mock.get.side_effect = PyMongoError
    objects_mock.create.side_effect = PyMongoError

    response = authorized_client.post('/api/geoip/', json=data)
    assert response.status_code == 503


def test_geoip_get(authorized_client, mock_get_ips_for_host, mock_ipstack):
    # prepare db
    data = populate_db()

    # test
    for key_value in data:
        key, value = list(key_value.items())[0]

        response = authorized_client.get(f'/api/geoip/{key}/{value}')
        content = ipstack_mock_response_content(value)

        assert response.status_code == 200
        response.json['ip'] = response.json.pop('_id')
        assert response.json in content


def test_geoip_get_not_existing(authorized_client):
    # prepare db
    populate_db()

    response = authorized_client.get(f'/api/geoip/url/www.notexisting.com')
    assert response.status_code == 404

    response = authorized_client.get(f'/api/geoip/ip/www.notexisting.com')
    assert response.status_code == 404


def test_geoip_delete(authorized_client, mock_get_ips_for_host):

    for reverse in (True, False):
        # prepare db
        data = populate_db()

        # test
        for key_value in sorted(data, key=lambda _key_value: list(_key_value.items())[0], reverse=reverse):
            key, value = list(key_value.items())[0]

            response = authorized_client.delete(f'/api/geoip/{key}/{value}')

            assert response.status_code == 204 if (key == 'url' and reverse) else 404

        assert GeoIP.objects.count() == 0
