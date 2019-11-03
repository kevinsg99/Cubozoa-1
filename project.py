import googlemaps
import geocoder
from datetime import datetime
from flask import Flask, render_template
from queue import LifoQueue
from googlemaps import convert
from googlemaps import directions

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
#home = (coordinates[0], coordinates[1])
home = (40.006066, -83.009263)
neighbor1 = (40.026252, -83.027001)
neighbor2 = (40.025054, -83.041613)
neighbor3 = (40.052468, -83.041610)
#route = LifoQueue()
allRoutes = LifoQueue()
#totalDist = 0
#streetDist = 0
#runDistance = 4
#adjStreet = gmaps.nearest_roads(home)[0]
adjStreet = []
adjStreet.append(gmaps.nearest_roads(home)[0])
adjStreet.append(gmaps.nearest_roads(neighbor1)[0])
adjStreet.append(gmaps.nearest_roads(neighbor2)[0])
adjStreet.append(gmaps.nearest_roads(neighbor3)[0])
#print(adjStreet)
'''
addressInfo = gmaps.reverse_geocode(home)
streetCoords = adjStreet[0]['location']
streetAddress = gmaps.reverse_geocode((streetCoords['latitude'], streetCoords['longitude']))
street = streetAddress[1]['address_components'][1]['long_name']
'''
#print(street)

def getMiles(coord1, coord2):
    direct = gmaps.directions(coord1, coord2)
    directLegs = direct[0]['legs']
    directDistance = directLegs[0]['distance']
    directText = directDistance['text']
    miles = ""
    done = False
    for s in directText:
        if (s == " "):
            done = True
        elif (done == False) and (s != " "):
            miles += s
    return float(miles)

miles = getMiles(home, neighbor1)

@app.route('/router/<runDistance><current>', methods=['GET'])
def router(current, adjacent, runDistance):
    print("hi")
    totalDist = 0
    streetDist = getMiles(current,adjacent[0]['location'])
    current = adjacent[0]['location']
    route = LifoQueue()
    while len(adjacent)-1 > 0:
        n = adjacent[0]
        print(n)
        if (home not in n) and (totalDist+streetDist < runDistance):
            route.put(n)
            print("-------------------------route: ------------------------------")
            print(route.qsize())
            '''temp = route
            i=0
            while i < temp.qsize():
                print(temp.get())
                i = i+1'''
            adjacent.pop(0)
            totalDist += streetDist
            router(current, adjacent, runDistance)
        elif (home in n) and (totalDist+streetDist == runDistance):
            route.put(n)
            allRoutes.put(route)
            route.get()

router(home, adjStreet, 4)

if __name__ == "__main__":
    app.run(debug=False)
    #router(adjStreet)