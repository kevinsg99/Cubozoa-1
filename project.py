import geocoder
import googlemaps
import geocoder
from datetime import datetime
from flask import Flask

app = Flask(__name__)

<<<<<<< HEAD
gmaps = googlemaps.Client(key="AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8")
=======
gmaps = googlemaps.Client(key='AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8')
>>>>>>> 46cfcb7304b769f5bedb72f4d04de39e22f075f0

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

#gets current location, returning array of coordinates
def getCurrentLocation():
    g = geocoder.ip('me')
    coordinates = g.latlng
    return coordinates
