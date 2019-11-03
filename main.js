(function myFunction() {

    function display(id, value) {
        document.getElementById(id).style.display = value;
    }

    function click(id, fn) {
        document.getElementById(id).addEventListener("click", fn);
    }

    document.addEventListener("DOMContentLoaded", function() {
        
        click("backButton", function() {
            display("userInput", "block");
            display("returnedRoutes", "none");
        });

        click("goButton", function() {
            display("userInput", "none");
            display("returnedRoutes", "block");
        });
    });

    function showMap() {
        var path = [map.google_coordinates];
        var center = new google.maps.LatLng(map.center[0], map.center[1]);
        var zoom = map.zoom;
   
        map = new google.maps.Map(document.getElementById("map-canvas"), {
            zoom: zoom,
            center: center,
            mapTypeId: 'terrain'
        });
   
        var activity_route = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: '#550FFF',
            strokeOpacity: 1.0,
            strokeWeight: 3,
            map: map
        });
   
        var start = new google.maps.Marker({
           position: path[0],
           map: map,
           label: 'S',
           fillColor:'green'
        });
   
        var end = new google.maps.Marker({
           position: path[path.length-1],
           map: map,
           label: 'E'
         });
      }

}())