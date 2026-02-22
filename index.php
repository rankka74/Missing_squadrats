
<!DOCTYPE html>
<html>
<head>

<!-- Initializing  Leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossorigin=""/>

<!-- Make sure you put this AFTER Leaflet's CSS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
     integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
     crossorigin=""></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-ajax/2.1.0/leaflet.ajax.min.js"></script>

<style>
#map { height: 80vh;
width: 80%}
</style>

</head>
<body>

<p>
<h1>A squadratinhos map layer for Garmin</h1>

<form action="upload.php" method="post" enctype="multipart/form-data">
  ID
  <input type="text" id="name" name="name" required><br>
  Select kml-file to upload:
  <input type="file" name="fileToUpload" id="fileToUpload" required><br>
  Coordinates NW lon
  <input type="text" id="NWlon" name="NWlon" value="22.1">
  NW lat
  <input type="text" id="NWlat" name="NWlat" value="61.6">
  SE lon
  <input type="text" id="SElon" name="SElon" value="26.2">
  SE lat
  <input type="text" id="SElat" name="SElat" value="59.8"><br>
  <input type="checkbox" id="cookie" name="cookie" value="cookie">
  <label for="cookie"> Save map location into a cookie</label><br>
  <input type="submit" id="submitButton" value="Upload kml file" name="submit"><br>
  Total number of squadratinhos on map area: <span id="tilesNumber"></span><!--  , NWlon: <span id="NWlonNumber"></span>, NWlat: <span id="NWlatNumber"></span>, NWlon: <span id="SElonNumber"></span>, NWlat: <span id="SElatNumber"></span> -->
<!--  <button type="button" onclick="submitForm()" id="clk">Submit</button> -->
</form>

<hr>

<p>

<div id="map"></div>

<hr>

<p>Img files:
<UL>

<?php

# https://stackoverflow.com/questions/21416793/deleting-3-days-old-file-from-folder-in-php
$imgFiles = glob("img/*");
$shFiles = glob("../../jobs/missing_squadrats/*.kml");
$threshold = strtotime('-1 day');
foreach ($imgFiles as $file) {
    if (is_file($file)) {
        if ($threshold < filemtime($file)) {
			echo "<LI><A href=\"https://oranta.kapsi.fi/missing_squadrats/" . $file . "\">" . str_replace("img/","",$file) . "</A><BR>\r\n";
        }
    }
}
foreach ($shFiles as $file) {
    if (is_file($file)) {
		echo "<LI>" . str_replace("../../jobs/missing_squadrats/","",$file) . "<BR>\r\n";
	}
}
?>

</UL>

<hr>

<p>Short instructions:
<ul>
<li>Download and save a kml-file of the visited squadratinhos from <a href="https://squadrats.com/">Squadrats</a> (Map - Download KML)
<li>Type the ID for your map (it can be your name or whatever)
<li>Zoom and pan the map above to the area you want the squadratinhos (default values gives you a map with about 46000 squadratinhos)
<li>Maximum number of squadratinhos for the map layer is <span id="maxNumberOfSquadrats"></span>. If there are more on the map, zoom in (in that case the "Upload kml file" button is not active)
<li>It's also possible to give the NW and SE corner coordinates manually
<!-- <li>Convert your kml-file to osm-file using your computer
<ul>
<li>Open the kml-file with text editor, for example <a href="https://notepad-plus-plus.org/">Notepad++</a>
<li>Copy everything (ctrl-a ctrl-c) to clip board
<li>Paste (ctrl-p) to the left panel of the <a href="https://mapbox.github.io/togeojson/">https://mapbox.github.io/togeojson/</a>
<li>Wait some time until the conversion to geojson-file is done and appears to the roght panel
<li>Copy everything (ctrl-a ctrl-c) from the right panel to clip board
<li>Paste (ctrl-p) to the new text editor window
<li>Save it with the geojson-extension
<li>Install (if not installed yet) and open <a href="https://josm.openstreetmap.de/">JSOM</a>
<li>Drag just created geojson-file to JOSM window
<li>In the top right corner in the Layers-panel there is your geojson-file. Right-click it and select Save As...
<li>Save the file as osm-format
</ul> -->
<li>Check the box "Save map location into a cookie" if you your web browser to remember current map location
<li>Click "Upload kml file" and wait, until you'll see "Everything ok" page
<li>Go back to the main page. Your map file should be on the list above
<li>Download the img-file and copy it to your Garmin (to the Garmin directory, where all the other map images are also)
<li>Make sure that the new map is enabled. The name of the map is squadrats-yyyymmdd
<li>On the Garmin you'll see a grid (pink borders) of all the squadratinhos. Surrounded with thicker dark red line are areas where are unvisited squadratinhos
</ul>

<hr>

<p>Some screen shots:<br>
<IMG src="screenshot-sample.png">
<IMG src="screenshot-enable.png">

<hr>

<p>Tested devices:
<ul>
  <li>Garmin Edge 530
  <li>Garmin Edge 820
  <li>Garmin Edge 1030
  <li>Garmin Edge 1040
</ul>

<hr>

<p>ToDo:
<ul>
  <li>Fix the Img files list to be sorted by file date
  <li>Get rid of messy lines near the edges
  <li>Add the kml-file as an overlay to the selection map
  <li>Make a browser extension
  <li>Add required -attribute to the kml-file -field in the form
  <ul>
    <li>20250124 required -attribut is added
  </ul>
  <li>Increase the number of tiles limit
  <ul>
    <li>20250124 Limit is now 200k
  </ul>
  <li>Remove special characters in the kml-file name
  <ul>
    <li>20250124 Special characters are now removed from the kml-file name
  </ul>
</ul>

<hr>

<p>Developer: <A href="mailto:olli.ranta@gmail.com">Olli</A><br>
Version: 20250124
 
<script>

// var version = 20250124;
var maxNumberOfSquadrats = 200000;
document.getElementById("maxNumberOfSquadrats").innerHTML = maxNumberOfSquadrats;

// https://stackoverflow.com/questions/5968196/how-do-i-check-if-a-cookie-exists
function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    // because unescape has been deprecated, replaced with decodeURI
    //return unescape(dc.substring(begin + prefix.length, end));
    return decodeURI(dc.substring(begin + prefix.length, end));
}

// https://www.geeksforgeeks.org/how-to-get-cookie-by-name-in-javascript/
// https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie
function getCookieByName(name) {
  var rc = decodeURIComponent(document.cookie); //rc == result cookie
  const cookies = rc.split(";");
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

if (getCookie("MissingSquadrats") == null) {
	var latCenter = 60.24;
	var lonCenter = 24.90;
}
else {
	var data = JSON.parse(getCookieByName("MissingSquadrats"));
	var latCenter = data.latCenter;
	var lonCenter = data.lonCenter;
}

var map = L.map('map').setView([latCenter, lonCenter], 11);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var bounds = map.getBounds();
var northWest = bounds.getNorthWest();
var southEast = bounds.getSouthEast();
var tiles = countTiles(northWest.lng, northWest.lat, southEast.lng, southEast.lat);
updateForm(northWest.lng, northWest.lat, southEast.lng, southEast.lat);
document.getElementById("tilesNumber").innerHTML = tiles;
if (tiles > maxNumberOfSquadrats) {
	document.getElementById("submitButton").disabled = true;
} else {
	document.getElementById("submitButton").disabled = false;
}


// https://stackoverflow.com/questions/32734897/how-to-get-map-box-coordinates-from-marker-in-leaflet
map.on('moveend', function() {
    var bounds = map.getBounds();
    var northWest = bounds.getNorthWest();
    var southEast = bounds.getSouthEast();
//	alert("Number of tiles: " + tiles);
//	document.getElementById("NWlon").value = northWest.lng;
	var tiles = countTiles(northWest.lng, northWest.lat, southEast.lng, southEast.lat);
	updateForm(northWest.lng, northWest.lat, southEast.lng, southEast.lat);
	document.getElementById("tilesNumber").innerHTML = tiles;
//	document.getElementById("NWlonNumber").innerHTML = lon2tile(northWest.lng,14);
//	document.getElementById("NWlatNumber").innerHTML = lat2tile(northWest.lat,14);
//	document.getElementById("SElonNumber").innerHTML = lon2tile(southEast.lng,14);
//	document.getElementById("SElatNumber").innerHTML = lat2tile(southEast.lat,14);
	if (tiles > maxNumberOfSquadrats) {
		document.getElementById("submitButton").disabled = true;
	} else {
		document.getElementById("submitButton").disabled = false;
	}
	});

map.on('zoomend', function() {
    var bounds = map.getBounds();
    var northWest = bounds.getNorthWest();
    var southEast = bounds.getSouthEast();
//	alert("Number of tiles: " + tiles);
//	document.getElementById("NWlon").value = northWest.lng;
	var tiles = countTiles(northWest.lng, northWest.lat, southEast.lng, southEast.lat);
	updateForm(northWest.lng, northWest.lat, southEast.lng, southEast.lat);
	document.getElementById("tilesNumber").innerHTML = tiles;
	if (tiles > maxNumberOfSquadrats) {
		document.getElementById("submitButton").disabled = true;
	} else {
		document.getElementById("submitButton").disabled = false;
	}
	});

function updateForm(northWestLng, northWestLat, southEastLng, southEastLat) {
	document.getElementById("NWlon").value = northWestLng;
	document.getElementById("NWlat").value = northWestLat;
	document.getElementById("SElon").value = southEastLng;
	document.getElementById("SElat").value = southEastLat;
	return;
}

function countTiles(northWestLng, northWestLat, southEastLng, southEastLat) {
	var tilesLon = lon2tile(southEastLng,17) - lon2tile(northWestLng,17);
	var tilesLat = lat2tile(southEastLat,17) - lat2tile(northWestLat,17);
	var tiles = tilesLon * tilesLat;
	return(tiles);
}

//function submitForm() { 
//	document.getElementById("clk").disabled = true;
//	return;
//}

// https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#ECMAScript_(JavaScript/ActionScript,_etc.)
function lon2tile(lon,zoom) {
	return (Math.floor((lon+180)/360*Math.pow(2,zoom)));
}
function lat2tile(lat,zoom) {
	return (Math.floor((1-Math.log(Math.tan(lat*Math.PI/180) + 1/Math.cos(lat*Math.PI/180))/Math.PI)/2 *Math.pow(2,zoom)));
}

</script>

</body>
</html>
