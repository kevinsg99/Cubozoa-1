import googlemaps
import geocoder
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    data = open('index.html').read()    
    return data

gmaps = googlemaps.Client(key='AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8')
home = [0.00, 0.00]
coordinates = [0.00,0.00]

######################################################################################
# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
#                                     mode="transit",
#                                     departure_time=now)
######################################################################################

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

if __name__ == "__main__":
    app.run(debug=True)
    router(adjStreet)