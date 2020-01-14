import pytest
from mongoengine import NotUniqueError
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

from backend.models import GeoIP
from backend.tests.conftest import ipstack_mock_response_content


def populate_db():
    data = [
        {'url': 'www.youtube.com'},
        {'url': 'www.wp.pl'},
        {'ip': '212.77.98.9'},
        {'ip': '2a00:1450:401b:803::200e'},
    ]

    for key_value in data:
        key, value = list(key_value.items())[0]

        content = ipstack_mock_response_content(value)
        for elem in content:
            try:
                GeoIP.objects.create(**elem)
            except NotUniqueError:
                pass
    return data


@pytest.mark.parametrize('data', [
    # ({'url': 'www.youtube.com'}),
    # ({'url': 'www.wp.pl'}),
    ({'ip': '212.77.98.9'}),
    ({'ip': '2a00:1450:401b:803::200e'}),
])
def test_geoiplist_post(client, clean_db, mock_ipstack, mock_get_ips_for_host, data):
    response = client.post('/api/geoip/', json=data)

    # 'ip' from ipstack response becomes '_id' in mongodb
    for elem in response.json:
        elem['ip'] = elem.pop('_id')

    assert response.status_code == 201

    assert all(elem in response.json for elem in ipstack_mock_response_content(list(data.values())[0]))

    response = client.post('/api/geoip/', json=data)
    for elem in response.json:
        elem['ip'] = elem.pop('_id')

    assert response.status_code == 302
    assert response.json == []


@pytest.mark.parametrize('data', [
    ({'url': 'www.youtube.com'}),
    ({'url': 'www.wp.pl'}),
    ({'ip': '212.77.98.9'}),
])
def test_geoiplist_post_ipstack_unavailable(client, clean_db, mock_ipstack_unavailable, data):
    response = client.post('/api/geoip/', json=data)

    assert response.status_code == 503


@pytest.mark.parametrize('data', [
    ({'url': 'www.youtube.com'}),
    ({'url': 'www.wp.pl'}),
    ({'ip': '212.77.98.9'}),
])
def test_geoiplist_post_db_unavailable(client_no_db_mock, mocker, mock_ipstack, mock_get_ips_for_host, data):
    mocker.patch('pymongo.topology.Topology.select_server', side_effect=ServerSelectionTimeoutError)
    objects_mock = mocker.patch('backend.models.GeoIP.objects')
    objects_mock.get.side_effect = PyMongoError
    objects_mock.create.side_effect = PyMongoError

    response = client_no_db_mock.post('/api/geoip/', json=data)
    assert response.status_code == 503


def test_geoip_get(client, clean_db, mock_get_ips_for_host, mock_ipstack):
    # prepare db
    data = populate_db()

    # test
    for key_value in data:
        key, value = list(key_value.items())[0]

        response = client.get(f'/api/geoip/{key}/{value}')
        content = ipstack_mock_response_content(value)
        response.json['ip'] = response.json.pop('_id')

        assert response.status_code == 200
        assert response.json in content


def test_geoip_get_not_existing(client, clean_db):
    # prepare db
    populate_db()

    response = client.get(f'/api/geoip/url/www.notexisting.com')
    assert response.status_code == 404

    response = client.get(f'/api/geoip/ip/www.notexisting.com')
    assert response.status_code == 404


def test_geoip_delete(client, clean_db, mock_get_ips_for_host):

    for reverse in (True, False):
        # prepare db
        data = populate_db()

        # test
        for key_value in sorted(data, key=lambda _key_value: list(_key_value.items())[0], reverse=reverse):
            key, value = list(key_value.items())[0]

            response = client.delete(f'/api/geoip/{key}/{value}')

            assert response.status_code == 204 if (key == 'url' and reverse) else 404

        assert GeoIP.objects.count() == 0
