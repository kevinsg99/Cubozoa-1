import googlemaps
import geocoder
from datetime import datetime
from flask import Flask, render_template
import queue

app = Flask(__name__)

@app.route("/")
def home():
    data = open('index.html').read()    
    return data

client = googlemaps.Client(key='AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8')
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
    g = geocoder.ip('me')
    #address = "1739 N High Street, Columbus, OH 43210"
    #g = geocoder.google(address)
    coordinates = g.latlng
    return coordinates

coordinates = getCurrentLocation()
print(coordinates)
#home = [{"lat" : coordinates[0], "lng" : coordinates[1]}, "Columbus"]
home = (coordinates[0], coordinates[1])
route = queue.LifoQueue()
allRoutes = queue.LifoQueue()
totalDist = 0
streetDist = 0
runDistance = 0
adjStreet = googlemaps.roads.nearest_roads(client, home)
print(adjStreet)
streetCoords = adjStreet[0]['location']
streetAddress = client.reverse_geocode((streetCoords['latitude'], streetCoords['longitude']))
streetverbose = streetAddress[1]
streetname = streetverbose['address_components'][1]['long_name']

#print(adjStreet)

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
    app.run(debug=False)
    router(adjStreet)