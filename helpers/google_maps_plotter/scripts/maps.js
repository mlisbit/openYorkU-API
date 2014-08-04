var map;

var markers = [];
var boundries = "";

var markers_showing = true

//http://gmaps-samples-v3.googlecode.com/svn/trunk/styledmaps/wizard/index.html
var styles = [
	{
		"featureType": "all",
		"elementType": "labels",
    	"stylers": [
			{ "visibility": "on"}, 
		],
	},
	{
		"featureType": "poi",
		"elementType": "labels",
		"stylers": [
		  { "visibility": "off" }
		]
	},
	{
		"featureType": "transit.station",
		"elementType": "labels",
		"stylers": [
		  { "visibility": "off" }
		]
	},
	
	{
   		"featureType": "road",
		"elementType": "labels",
    	"stylers": [{ "visibility": "on" }]
	},
];

var weird_glitch_in_my_IDE_requires_this_to_be_here_for_syntax_highlights = ['pointless'];

function initialize() {
	var york_campus = new google.maps.LatLng(43.774543, -79.501192);
	var mapOptions = {
		zoom: 17,
		center: york_campus,
		styles:styles
	};
	map = new google.maps.Map(document.getElementById('map-canvas'),
	  	mapOptions
	);

	// This event listener will call addMarker() when the map is clicked.
	google.maps.event.addListener(map, 'click', function(event) {
		if (document.getElementById('markit').checked) {
			addMarker(event.latLng);
		}
	});
	
	drawBoundries();
}


function drawBoundries() {
	var york_boundry_markers = [
		[43.776237865203065, -79.51681137084961],
		[43.775075844980215, -79.51640367507935], 
		[43.773681390906226, -79.51503038406372], 
		[43.77194602487057, -79.51376438140869], 
		[43.76858360987894, -79.50979471206665], 
		[43.771860804705604, -79.49337959289551], 
		[43.7781435294857, -79.49496746063232],
		[43.780405458665726, -79.49447393417358],
		[43.781273025234945, -79.49464559555054],
		[43.776237865203065, -79.51681137084961]
	];
	var york_boundry = [];
	var world_boundry = [
    	new google.maps.LatLng(-400.27770503961696, -151.171875),
		new google.maps.LatLng(-400.44032649527307, 133.59375),
		new google.maps.LatLng(-400.683528083787756, 132.1875),
		new google.maps.LatLng(-400.94304553343818, 0.28125),
  	];
		
	for (var i = 0; i < york_boundry_markers.length; i++) {
		york_boundry.push(new google.maps.LatLng(york_boundry_markers[i][0], york_boundry_markers[i][1]));
	}

	var shape = new google.maps.Polygon({
		paths: [world_boundry, york_boundry],
		strokeColor: '#363636',
		strokeOpacity: 0.8,
		strokeWeight: 2,
		fillColor: '#000000',
		fillOpacity: 0.35
	});

	shape.setMap(map);
}
// Add a marker to the map and push to the array.

var iw = new google.maps.InfoWindow({
	content: ''
});
function draw(type) {
	if (type === 'restaurants') {
		restaurants = new LocationPlotter({file: 'restaurant_extended_list.txt', type: 'restaurants'})
		restaurants.add()
	} else if (type === 'building_covers') {
		restaurants = new LocationPlotter({file: 'restaurant_extended_list.txt', type: 'restaurants'})
		restaurants.add()
	} else if (type === 'building_location') {
		restaurants = new LocationPlotter({file: 'restaurant_extended_list.txt', type: 'restaurants'})
		restaurants.add()
	} else if (type === 'parking') {
		restaurants = new LocationPlotter({file: 'restaurant_extended_list.txt', type: 'restaurants'})
		restaurants.add()
	} else if (type === 'recreational') {
		restaurants = new LocationPlotter({file: 'restaurant_extended_list.txt', type: 'restaurants'})
		restaurants.add()
	}
}
function addMarker(location, label) {
	
		var marker = new google.maps.Marker({
			position: location,
			map: map,
			title: label,
       		iw: label
		});
		
		google.maps.event.addListener(marker, "click", function (e) { 
			iw.content = this.iw
			iw.open(map, this); 
		});
		markers.push(marker);
	
}

// Sets the map on all markers in the array.
function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function toggleMarkers() {
	if (markers_showing) {
		markers_showing = false;
		setAllMap(map);
	} else {
		markers_showing = true;
		setAllMap(null);
	}
}
// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  
}

// Shows any markers currently in the array.
function showMarkers() {
  
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}

function printMarkers() {
	for (i in markers) {
		console.log(markers[i].position.toString(), markers[i].iw)
	}
	//http://maps.vasile.ch/geomask/
	//http://www.ttu.edu/map/
}

google.maps.event.addDomListener(window, 'load', initialize);