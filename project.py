import googlemaps
from datetime import datetime
from flask import Flask

app = Flask(__name__)

gmaps = googlemaps.Client(api_key='AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))


class profile:
    distance = input('distance:')
    location = geocoder.ip('me')
