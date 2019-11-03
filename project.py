import googlemaps
import geocoder
from datetime import datetime
from flask import Flask, render_template
from queue import LifoQueue
from googlemaps import convert
import requests

app = Flask(__name__)

gmaps = googlemaps.Client(key="AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8")
mq_KEY = "iDccP1485vRS7TK0BzhNqXc6fro7ckuD"

app = Flask(__name__)

@app.route("/")
def home():
    data = open('index.html').read()    
    return data

home = [0.00, 0.00]
coordinates = [0.00,0.00]

#determines with some margin of error all the intersections and their coordinates over blanket area
#blanket area: (run_distance^2/4)
def sweep(home, spacing):
    grid = [home]
    row=1
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column < 5280*runDistance/2.0:
            grid.append([home[0]+spacing*column,home[1]])
            row+=1
        grid.append([home[0],home[1]+column*spacing])
        column+=1
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column < 5280*runDistance/2.0:
            grid.append([home[0]-spacing*column,home[1]])
            row+=1
        grid.append([home[0],home[1]+column*spacing])
        column+=1
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column > -5280*runDistance/2.0:
            grid.append([home[0]+spacing*column,home[1]])
            row+=1
        grid.append([home[0],home[1]-column*spacing])
        column+=1
    while 30*row > -5280*runDistance/2.0:
        column=1
        while 30*column > 5280*runDistance/2.0:
            grid.append([home[0]-spacing*column,home[1]])
            row+=1
        grid.append([home[0],home[1]-column*spacing])
        column+=1
    intersections = []
    for i in range(len(grid)):
        requested_info = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?key="
        + mq_KEY + "&location=" 
        + str(grid[i][0])
        + ","
        + str(grid[i][1])
        + "&includeRoadMetadata=true&includeNearestIntersection=true")
        intersection_coordinates = [requested_info.json()['results'][0]['providedLocation']['latLng']['lat'],requested_info.json()['results'][0]['providedLocation']['latLng']['lng']]
        intersections.append(intersection_coordinates)
    print(intersections)
    return intersections

#gets current location, returning array of coordinates
def getCurrentLocation():
    g = geocoder.ip('me')
    coordinates = g.latlng
    #address = "1739 N High St, Columbus, OH 43210"
    #lat, lng = gmaps.address_to_latlng(address)
    #result = [lat, lng]
    #print(result)
    return coordinates

#coordinates = getCurrentLocation()
#print(coordinates)
#home = [{"lat" : coordinates[0], "lng" : coordinates[1]}, "Columbus"]
#home = (coordinates[0], coordinates[1])
home = (40.006066, -83.009263)
route = LifoQueue()
allRoutes = LifoQueue()
totalDist = 0
streetDist = 0
runDistance = 0
'''
adjStreet = gmaps.nearest_roads(home)
#print(adjStreet)
addressInfo = gmaps.reverse_geocode(home)
streetCoords = adjStreet[0]['location']
streetAddress = gmaps.reverse_geocode((streetCoords['latitude'], streetCoords['longitude']))
street = streetAddress[1]['address_components'][1]['long_name']
print(street)

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
'''
if __name__ == "__main__":
    #app.run(debug=False)
    #router(adjStreet)
    sweep(home, 0.005)