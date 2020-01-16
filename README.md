# Solution
I could not deploy to heroku - had a problem with dockhero plugin, which did not work for me and indicated reinstallation need everytime

# Task Definition
Summary
The aim of this task is to build an API (backed by any kind of database) that requires JWT authorization. The application should be able to store geolocation data in the database, based on IP address or URL - you can use https://ipstack.com/ to get geolocation data (you can obtain free API KEY here -> https://ipstack.com/signup/free). The API should be able to add, delete or provide geolocation data on the base of ip address or URL. 

## Application specification
It should be a RESTful API
You can use https://ipstack.com/ for the geolocation of IP addresses and URLs
The back-end application can be built in any framework of your choice
The application should preferably be hosted and available online (for example on Heroku - https://www.heroku.com/free)
Heroku also provides some free DBs so you can use them
It is preferable that the API operates using JSON (for both input and output)
You can create a registration form but using hardcoded values for authorization is also acceptable (just make sure that API is secured by JWT token)
Tests, serializers and docker are always welcome!

## How to submit
Create a public Git repository and share the link with us
Deploy the application so that it is available online and we can check how it works (again, can be using free plan on Heroku but any hosting option will work)

## Notes:
We will run the application on our local machines for testing purposes. This implies that the solution should provide a quick and easy way to get the system up and running, including test data (hint: you can add Docker support so we can run it easily)
We will test the behavior of the system under various "unfortunate" conditions (hint: How will the app behave when we take down the DB? How about the GeoIP API?)

