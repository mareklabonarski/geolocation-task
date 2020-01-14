curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "url": "http://www.wp.pl"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "url": "www.wp.pl"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "url": "http://www.wp.pl"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "ip": "212.77.100.83"}'

curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "url": "https://www.youtube.com"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "ip": "216.58.209.14"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -d '{ "ip": "216.58.209.14"}'

curl -X GET 'http://127.0.0.1/api/geoip/ip/216.58.209.14'
curl -X GET 'http://127.0.0.1/api/geoip/url/www.youtube.com'

curl -X GET 'http://127.0.0.1/api/geoip/ip/212.77.100.83'
curl -X GET 'http://127.0.0.1/api/geoip/url/www.wp.pl'

curl -X DELETE 'http://127.0.0.1/api/geoip/ip/212.77.100.83'
curl -X DELETE 'http://127.0.0.1/api/geoip/url/www.youtube.com'
curl -X DELETE 'http://127.0.0.1/api/geoip/url/www.wp.pl'
