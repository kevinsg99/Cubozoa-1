import geocoder
import googlemaps
from datetime import datetime
from flask import Flask
from queue import LifoQueue

app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8')
home = [0.00, 0.00]
coordinates = [0.00,0.00]

#points = [{"lat" : -33.867486, "lng" : 151.206990}, "Sydney"]

#gets current location, returning array of coordinates
def getCurrentLocation():
    #g = geocoder.ip('me')
    #coordinates = g.latlng
    address = "1739 N High St, Columbus, OH 43210"
    lat, lng = gmaps.address_to_latlng(address)
    print(result)
    #coordinates = [lat, lng]
    return coordinates

coordinates = getCurrentLocation()
print(coordinates)
#home = [{"lat" : coordinates[0], "lng" : coordinates[1]}, "Columbus"]
home = (coordinates[0], coordinates[1])
route = LifoQueue()
allRoutes = LifoQueue()
totalDist = 0
streetDist = 0
runDistance = 0
adjStreet = gmaps.nearest_roads(home)
print(adjStreet)

def router(adjacent):
    for n in adjacent:
        #print(n)
        if (home not in n) and (totalDist+streetDist < runDistance):
            route.put(n)
            router(n)
        elif (home in n) and (totalDist+streetDist == runDistance):
            route.put(n)
            allRoutes.put(route)
            route.get()

router(adjStreet)