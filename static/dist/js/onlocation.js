//Global variables
var map;
var waypoints;
var longitude;
var latitude;
var location;
var autocomplete_address;
      
var movie_latlong=[];
var bounds;
var markers=[];
var iterator;
var infowindow = null;
var thismap_center;
var thismap_zoom;
var allcontent = [];

function loadScript() {
    // Load Google maps API (?) and execute initialize()
    //src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCrN_qDQmG0UNOVl9QZWXnKvueP8xPlEwU&sensor=true">
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=true&callback=initialize&libraries=places';
    document.body.appendChild(script);
};
      
function initialize() {
  var URL = document.URL;
  var load_maps = false;
  if (URL.search('altsearch')>0) {
    load_maps = true;
  }
  else if (URL.search('about')>0) {
    load_maps=false;
  }
  else {
      autocomplete_address = new google.maps.places.Autocomplete(
        /** @type {HTMLInputElement} */(document.getElementById('address_search')),
        { types: ['geocode'] });
      geocoder = new google.maps.Geocoder();
      load_maps=true;
  }

  if (load_maps==true) {
      var la = new google.maps.LatLng(34.101509, -118.32691);
    iterator = 0;
    var mapOptions = {
    center: la,
    zoom: 12,
    streetViewControl: false
  }

  }
        
  map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
  google.maps.event.addDomListener(window, 'load', initialize);
  //google.maps.event.addListener(autocomplete_address, 'place_changed', function() {
  //  getMovie();
  //});
  
  infowindow = new google.maps.InfoWindow({
    content: "holding..."
  });

}

// Drop the markers
function drop() {
  deleteMarkers();
  dropMarkerlist();
}

// Adjusting the map such that the markers are visible.
function seeMarkers() {
  bounds = map.getBounds();
  var min_lat = map.getCenter().lat();
  var max_lat = map.getCenter().lat();
  var min_lng = map.getCenter().lng();
  var max_lng = map.getCenter().lng();

  for (var i=0; i<movie_latlong.length; i++) {

  // Some functionality to recenter the map
    thislat = movie_latlong[i].lat();
    thislng = movie_latlong[i].lng();
    
    if (thislat<min_lat) {
      min_lat = thislat;
    }
    if (thislat>max_lat) {
      max_lat = thislat;
    }
    if (thislng<min_lng) {
      min_lng = thislng;
    }
    if (thislng>max_lng) {
      max_lng = thislng;
    }
  }
        
  var sw = new google.maps.LatLng(min_lat, min_lng); 
  var ne = new google.maps.LatLng(max_lat, max_lng);
  var newbounds = new google.maps.LatLngBounds(sw,ne);
  map.fitBounds(newbounds);
  thismap_center = map.getCenter();
  thismap_zoom = map.getZoom();
}
    

// Create LatLng objects from the returned list of latitudes and longitudes for a movie.
function dropMarkerlist(){
  // Get the locations from the database
  var movie = $('#moviesearch').val();
  $.get('/locations?title='+movie, function(result) {
    var quickcheck = eval(result)
      if (!(quickcheck[0][0]==="Title not found")) {
        makeMarkers(result);
        console.log(result);
        // Adjust the map so you can see the markers
        seeMarkers();
        
        // Drop the markers
        for (var i = 0; i < movie_latlong.length; i++) {
          setTimeout(function() {
            markers = addMarker();
          }, i * 200);
        }
      }
      else {
        $('#moviesearch').val('Title not found');
      }
  });
}
      

// Create the Marker objects
function addMarker() {
  marker = new google.maps.Marker({
  position: movie_latlong[iterator],
  map: map,
  draggable: false,
  animation: google.maps.Animation.DROP,
  html: allcontent[iterator]
  });
  markers.push(marker);
  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(this.html);
    infowindow.open(map, this);
  });
  google.maps.event.addListener(infowindow, "closeclick", function(){
    map.panTo(thismap_center);
    map.setZoom(thismap_zoom);
  });
  iterator++;
  return markers;
}

// Clear all the current markers from the map
function clearMarkers() {
  setAllMap(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  movie_latlong = [];
  markers = [];
  allcontent = [];
  iterator = 0;
} 

// Set the values of markers
function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  } 
}

// Script to get movies near me
function getMovie() {
  deleteMarkers()
  var address = document.getElementById('address_search').value;
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 10
          }
      });
      markers.push(marker);
      dropNearbyMovies(results[0].geometry.location)
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  }); 
}

// Create LatLng objects from the returned list of latitudes and longitudes for a movie.
function dropNearbyMovies(LatLongObject){
  // Get the locations from the database
    console.log(LatLongObject);
    latitude = LatLongObject.k
    longitude = LatLongObject.A
    $.get('/nearby?latitude='+latitude+'&longitude='+longitude, function(result) {
    // Make the marker and info windows
    makeMarkers(result);
    // Adjust the map so you can see the markers
    seeMarkers();
  
  // Drop the markers
  for (var i = 0; i < movie_latlong.length; i++) {
    setTimeout(function() {
      markers = addMarker();
    }, i * 200);
  }
  });
}

// Here I am creating the Google markers from lat/long pairs and getting the information about the movie location into
// the info windows.
function makeMarkers(result){
      JSONwaypoints = eval(result);
      console.log(JSONwaypoints);
    // Make an array of lat/long coordinates from those locations
    for (pair in JSONwaypoints) {
      latitude = JSONwaypoints[pair][pair][1];
      longitude = JSONwaypoints[pair][pair][2];
      thislatlong = [latitude,longitude];
      movie_latlong.push(new google.maps.LatLng(latitude, longitude));
      var sv_url1 = 'http://maps.googleapis.com/maps/api/streetview?size=300x200&location=';
      //var sv_location = latitude+','+longitude;
      var sv_location = JSONwaypoints[pair][pair][5];
      var sv_url2 = '&sensor=false';
      var sv_url = sv_url1+sv_location+sv_url2;
      var url = JSONwaypoints[pair][pair][4];
      var infocontent = '<div id="infowindow"><h2 id="infotitle"><b>'+JSONwaypoints[pair][pair][0]+'</b></h2>' +
        '<h4 id="infotext"><b>Scene description: </b>'+JSONwaypoints[pair][pair][3]+'<br>' +
        '<b>Address: </b>'+JSONwaypoints[pair][pair][5]+'</h4><br>' +
        '<center><img src="'+url+ '" alt="movie poster" height="200px" style="margin-right:5px">' +
        '<img src="'+sv_url+'" alt="street view" height="200px"></center></div>';
      allcontent.push(infocontent);
    }
}