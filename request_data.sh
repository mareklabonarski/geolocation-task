sudo apt install jq -y
token=$( curl -s -X POST 'http://127.0.0.1/auth' -H 'Content-Type: application/json' -d '{ "username": "sofomo", "password": "sofomo"}' | jq -r  '.access_token' )
echo $token

curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "url": "http://www.wp.pl"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "url": "www.wp.pl"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "url": "http://www.wp.pl"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "ip": "212.77.100.83"}'

curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "url": "https://www.youtube.com"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "ip": "216.58.209.14"}'
curl -X POST 'http://127.0.0.1/api/geoip/' -H 'Content-Type: application/json' -H "Authorization: JWT $token" -d '{ "ip": "216.58.209.14"}'

curl -X GET -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/ip/216.58.209.14'
curl -X GET -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/url/www.youtube.com'

curl -X GET -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/ip/212.77.100.83'
curl -X GET -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/url/www.wp.pl'

curl -X DELETE -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/ip/212.77.100.83'
curl -X DELETE -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/url/www.youtube.com'
curl -X DELETE -H "Authorization: JWT $token" 'http://127.0.0.1/api/geoip/url/www.wp.pl'
