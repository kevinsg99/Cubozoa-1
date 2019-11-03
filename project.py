import googlemaps
import geocoder
from datetime import datetime
from flask import Flask, render_template
from queue import LifoQueue
from googlemaps import convert
from googlemaps import directions
import socket

app = Flask(__name__)
gmaps = googlemaps.Client(key="AIzaSyAsLI9pzus4z91Pyq1_aANnpOa8YKzE2t8")
mq_KEY = 'iDccP1485vRS7TK0BzhNqXc6fro7ckuD'
socket.setdefaulttimeout(9)
@app.route("/")
def home():
    #data = open('templates/index.html').read()    
    #return data
    return render_template('index.html')

home = [0.00, 0.00]
coordinates = [0.00,0.00]

#determines with some margin of error all the intersections and their coordinates over blanket area
#blanket area: (run_distance^2/4)
def sweep(home, spacing):
    grid = [home]
    row=1
    #1 quadrant
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column < 5280*runDistance/2.0:
            grid.append([home[0]+spacing*column,home[1]])
            row+=1
            column+=1
        grid.append([home[0],home[1]+column*spacing])
        
    row=1
    print('1Q'+str(grid))
    #4th quadrant
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column < 5280*runDistance/2.0:
            grid.append([home[0]+spacing*column,home[1]])
            row+=1
            column+=1
        grid.append([home[0],home[1]-column*spacing])
        
    row=1
    print('4Q'+str(grid))
    #3rd quadrant
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column < 5280*runDistance/2.0:
            grid.append([home[0]-spacing*column,home[1]])
            row+=1
            column+=1
        grid.append([home[0],home[1]-column*spacing])      
    row=1
    print('3Q'+str(grid))
    #2nd quadrant
    while 30*row < 5280*runDistance/2.0:
        column=1
        while 30*column < 5280*runDistance/2.0:
            grid.append([home[0]-spacing*column,home[1]])
            row+=1
            column+=1
        grid.append([home[0],home[1]+column*spacing])
    print('2Q'+str(grid))

    intersections = []

    for i in range(len(grid)):
        '''
        requested_info = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?key="
        + mq_KEY + "&location=" 
        + str(grid[i][0])
        + ","
        + str(grid[i][1])
        + "&includeRoadMetadata=true&includeNearestIntersection=true")
        '''
        requested_info = geocoder.mapquest([grid[i][0], grid[i][1]],method='reverse',key=mq_KEY)
        intersection_coordinates = [requested_info.json()['results'][0]['locations'][0]['nearestIntersection']['latLng']['latitude'],requested_info.json()['results'][0]['locations'][0]['nearestIntersection']['latLng']['longitude']]
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

#adjStreet.append(gmaps.nearest_roads(home)[0])
#adjStreet.append(gmaps.nearest_roads(neighbor1)[0])
#adjStreet.append(gmaps.nearest_roads(neighbor2)[0])
#adjStreet.append(gmaps.nearest_roads(neighbor3)[0])
#print(adjStreet)
'''
addressInfo = gmaps.reverse_geocode(home)
streetCoords = adjStreet[0]['location']
streetAddress = gmaps.reverse_geocode((streetCoords['latitude'], streetCoords['longitude']))
street = streetAddress[1]['address_components'][1]['long_name']
'''
#print(street)
#direct = gmaps.directions(home, neighbor1)

def getMiles(direct):
    directLegs = direct[0]['legs']
    directDistance = directLegs[0]['distance']
    directText = directDistance['text']
    print(directText)
    miles = ""
    done = False
    for s in directText:
        if (s == " "):
            done = True
        elif (done == False) and (s != " "):
            miles += s
    return miles

def router(adjacent):
    totalDist = 0
    while len(adjacent) > 0:
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
            router(adjacent)
        elif (home in n) and (totalDist+streetDist == runDistance):
            route.put(n)
            allRoutes.put(route)
            route.get()

if __name__ == "__main__":
    app.run(debug=False)
    home = (40.006066, -83.009263)
    route = LifoQueue()
    allRoutes = LifoQueue()
    totalDist = 0
    streetDist = 1
    runDistance = 4
    adjStreet = sweep(home,0.00005)
    router(adjStreet)
