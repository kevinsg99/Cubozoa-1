import googlemaps
import geocoder
from datetime import datetime
from flask import Flask, render_template
from queue import LifoQueue
from googlemaps import convert

app = Flask(__name__)

gmaps = googlemaps.Client(key="AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8")

@app.route("/")
def home():
    data = open('index.html').read()    
    return data

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
    coordinates = g.latlng
    #address = "1739 N High St, Columbus, OH 43210"
    #lat, lng = gmaps.address_to_latlng(address)
    #result = [lat, lng]
    #print(result)
    return coordinates

coordinates = getCurrentLocation()
#print(coordinates)
#home = [{"lat" : coordinates[0], "lng" : coordinates[1]}, "Columbus"]
home = (coordinates[0], coordinates[1])
home = (40.006066, -83.009263)
neighbor1 = (40.006066, -80.009263)
neighbor2 = (33.006066, -70.009263)
neighbor3 = (42.006066, -90.009263)
route = LifoQueue()
allRoutes = LifoQueue()
totalDist = 0
streetDist = 1
runDistance = 4
adjStreet = gmaps.nearest_roads([home, neighbor1, neighbor2, neighbor3])
#print(adjStreet)
'''
addressInfo = gmaps.reverse_geocode(home)
streetCoords = adjStreet[0]['location']
streetAddress = gmaps.reverse_geocode((streetCoords['latitude'], streetCoords['longitude']))
street = streetAddress[1]['address_components'][1]['long_name']
'''
#print(street)

def router(adjacent):
    print("hi")
    totalDist = 0
    while len(adjacent) - 1:
        n = adjacent[0]
        print(n)
        if (home not in n) and (totalDist+streetDist < runDistance):
            route.put(n)
            #print("route: ")
            #print(route.get())
            adjacent.pop()
            totalDist += streetDist
            router(adjacent)
        elif (home in n) and (totalDist+streetDist == runDistance):
            route.put(n)
            allRoutes.put(route)
            route.get()

router(adjStreet)

if __name__ == "__main__":
    app.run(debug=False)
    #router(adjStreet)