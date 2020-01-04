function createMap(bikeStations) {

// Create the tile layer that will be the background of our map
var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
  });

  // Create a baseMaps object to hold the lightmap layer
  var baseMaps = {
    "Light Map": lightmap
  };

  // Create an overlayMaps object to hold the bikeStations layer
  var overlayMaps = {
    "Bike Stations": bikeStations,
  };

  // Create the map object with options
  var map = L.map("map-id", {
    center: [41.8781, -87.6298],
    zoom: 12,
    layers: [lightmap, bikeStations]
  });

  // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(map);
  
}


function createMarkers(response) {

    // Pull the "stations" property off of response.data
    var stations = response;
  
    // Initialize an array to hold bike markers
    var bikeMarkers = [];

    // Loop through the stations array
    for (var index = 0; index < stations.length; index++) {
      var station = stations[index];

      var icons = {
        Start_Marker: L.ExtraMarkers.icon({
          icon: "ion-android-bicycle",
          iconColor: "white",
          markerColor: "green",
          shape: "circle"
        }),
        End_Marker: L.ExtraMarkers.icon({
          icon: "ion-android-bicycle",
          iconColor: "white",
          markerColor: "red",
          shape: "circle"
        })
      };
  
      // For each station, create a marker and bind a popup with the station's name
      var startMarker = L.marker([station.Latitude_x, station.Longitude_x], {
        icon: icons.Start_Marker
      });
      startMarker.bindPopup("Start Station ID" + "<br> <h3>" + station.station_a + "<h3>");

      var endMarker = L.marker([station.Latitude_y, station.Longitude_y], {
        icon: icons.End_Marker
      });
      endMarker.bindPopup("End Station ID" + "<br> <h3>" + station.station_b + "<h3>");
  
      // Add the marker to the bikeMarkers array
      bikeMarkers.push(startMarker);
      bikeMarkers.push(endMarker);

      // Create Polyline
      var pointA = new L.LatLng(station.Latitude_x, station.Longitude_x);
      var pointB = new L.LatLng(station.Latitude_y, station.Longitude_y);
      var pointList = [pointA, pointB];
  
      var firstpolyline = new L.Polyline(pointList, {
      color: 'blue',
      weight: 3,
      opacity: 0.5,
      smoothFactor: 1
      })
  
      bikeMarkers.push(firstpolyline);
    }
  
    // Create a layer group made from the bike markers array, pass it into the createMap function
    createMap(L.layerGroup(bikeMarkers));
    
}
  
  
// Perform an API call to the Citi Bike API to get station information. Call createMarkers when complete
var defaultURL = "/api/trips";
d3.json(defaultURL, createMarkers);