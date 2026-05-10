<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">

<!-- Initializing  Leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossorigin=""/>

<!-- Make sure you put this AFTER Leaflet's CSS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
     integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
     crossorigin=""></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-ajax/2.1.0/leaflet.ajax.min.js"></script>

<link rel="stylesheet" href="style.css">

</head>
<body>

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
  <label for="zoomLevel">Select a zoom level:</label>
  <select id="zoomLevel" name="zoomLevel">
    <option selected value="17">Squadratinhos</option>
    <option value="14">Squadrats</option>
  </select><br>
  Line color
  <input type="color" id="lineColor" name="lineColor" value="#853A3A">
  Line weight
  <input type="number" id="lineWeight" name="lineWeight" min="1" max="10" value="5"><br>
  <input type="submit" id="submitButton" value="Upload kml file" name="submit">
  <input type="checkbox" id="cookie" name="cookie" value="cookie">
  <label for="cookie"> Save map properties into a cookie</label><br>
  Total number of squadratinhos on map area: <span id="tilesNumber"></span><!--  , NWlon: <span id="NWlonNumber"></span>, NWlat: <span id="NWlatNumber"></span>, NWlon: <span id="SElonNumber"></span>, NWlat: <span id="SElatNumber"></span> -->
<!--  <button type="button" onclick="submitForm()" id="clk">Submit</button> -->
</form>

<div id="map"></div>

<p class="card-header card-header-files">Img files:
<UL class="card-body card-body-files">

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

<p class="card-header card-header-instructions">Short instructions:
<ul class="card-body card-body-instructions">
<li>Download and save a kml-file of the visited squadrats and squadratinhos from <a href="https://squadrats.com/">Squadrats</a> (Map - Download KML)
<li>Type the ID for your map (it can be your name or whatever)
<li>Select a zoom level, line color and weight and map aspect ratio
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
<li>Check the box "Save map location into a cookie" if you your web browser to remember the current map location
<li>Click "Upload kml file" and wait, until you'll see "Everything ok" page
<li>Go back to the main page. Your map file should be on the list above in 5 minutes
<li>Download the img-file and copy it to your Garmin (to the Garmin directory, where all the other map images are also)
<li>Make sure that the new map is enabled. The name of the map is squadrats-yyyymmdd
<li>On the Garmin you'll see the unvisited squadratinhos surrounded with thicker dark red line
</ul>

<p class="card-header card-standalone card-header-screenshots">Some screen shots:<br>
<IMG src="screenshot-sample.png">
<IMG src="screenshot-enable.png">

<p class="card-header card-header-devices">Tested devices:
<ul class="card-body card-body-devices">
  <li>Garmin Edge 530
  <li>Garmin Edge 820
  <li>Garmin Edge 840
  <li>Garmin Edge 1030
  <li>Garmin Edge 1040
  <li>Garmin Edge 1050
  <li>Garmin eTrex 30
</ul>

<p class="card-header card-header-todo">ToDo:
<ul class="card-body card-body-todo">
  <li>Add optional grid for whole map area
  <li>Fix the Img files list to be sorted by file date
  <li>Add the kml-file as an overlay to the selection map
  <li>Make a browser extension
  <li>User configurable map aspect ratio
  <ul>
    <li>20260510 Added user configurable map aspect ratio
  </ul>
  <li>User configurable tile line color and width
  <ul>
    <li>20260510 Added user configurable tile line color and width
  </ul>
  <li>Add an option to make a map of squadrats (zoom level 14)
  <ul>
    <li>20260510 Option for squadrats or squadratinhos
  </ul>
  <li>Get rid of messy lines near the edges
  <ul>
    <li>20260222 Only unvisited tiles on the map
  </ul>
  <li>Complete re-write
  <ul>
    <li>20260222 Only unvisited tiles on the map
  </ul>
  <li>Make zooming smoother
  <ul>
    <li>20250506 Changed zoomSnap and zoomDelta to 0.2, the default values were 1 for both
  </ul>
  <li>Remove special characters from the ID
  <ul>
    <li>20250506 Special characters are now removed from the ID
  </ul>
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

<p class="footer">Developer: <A href="mailto:olli.ranta@gmail.com">Olli</A><br>
Version: 20260510

<script>

// var version = 20250124;
var maxNumberOfSquadrats = 200000;
var zoomLevel = document.getElementById("zoomLevel").value
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
  var squadratinhosColor = "#853A3A";
  var squadratinhosLineWeight = 5;
  var squadratsColor = "#853A3A";
  var squadratsLineWeight = 5;
} else {
	var data = JSON.parse(getCookieByName("MissingSquadrats"));
  if (typeof data.mapCenterLat === 'undefined') {
    var latCenter = 60.24;
  }
  else {
    var latCenter = data.mapCenterLat;
  }
  if (typeof data.mapCenterLon === 'undefined') {
    var lonCenter = 24.90;
  }
  else {
    var lonCenter = data.mapCenterLon;
  }
  if (typeof data.squadratinhosColor === 'undefined') {
    var squadratinhosColor = "#853A3A";
  }
  else {
    var squadratinhosColor = data.squadratinhosColor;
    var lineColor = squadratinhosColor;
  }
  if (typeof data.squadratinhosLineWeight === 'undefined') {
    var squadratinhosLineWeight = 5;
  }
  else {
    var squadratinhosLineWeight = data.squadratinhosLineWeight;
    var lineWeight = squadratinhosLineWeight;
  }
  if (typeof data.squadratsColor === 'undefined') {
    var squadratsColor = "#853A3A";
  }
  else {
    var squadratsColor = data.squadratsColor;
  }
  if (typeof data.squadratsLineWeight === 'undefined') {
    var squadratsLineWeight = 5;
  }
  else {
    var squadratsLineWeight = data.squadratsLineWeight;
  }
}

// https://leafletjs.com/examples/zoom-levels/
var map = L.map('map', {
	center: [latCenter, lonCenter],
	zoom: 11,
	zoomDelta: 0.1,
    zoomSnap: 0.1
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var tiles = countTiles();
updateForm();
document.getElementById("tilesNumber").innerHTML = tiles;
if (tiles > maxNumberOfSquadrats) {
	document.getElementById("submitButton").disabled = true;
} else {
	document.getElementById("submitButton").disabled = false;
}
document.getElementById("lineColor").value = squadratinhosColor;
document.getElementById("lineWeight").value = squadratinhosLineWeight;

// https://stackoverflow.com/questions/32734897/how-to-get-map-box-coordinates-from-marker-in-leaflet
map.on('moveend', function() {
  countTiles();
  updateForm();
});

map.on('zoomend', function() {
  countTiles();
  updateForm();
});

// https://gomakethings.com/how-to-detect-all-changes-to-a-form-with-vanilla-javascript/
let select = document.querySelector('select');
select.addEventListener('input', function (event) {
  zoomLevel = document.getElementById("zoomLevel").value
  if (zoomLevel == 14) {
    squadratinhosColor = document.getElementById("lineColor").value
    squadratinhosLineWeight = document.getElementById("lineWeight").value
    document.getElementById("lineColor").value = squadratsColor;
    document.getElementById("lineWeight").value = squadratsLineWeight;
  } else if (zoomLevel == 17) {
    squadratsColor = document.getElementById("lineColor").value
    squadratsLineWeight = document.getElementById("lineWeight").value
    document.getElementById("lineColor").value = squadratinhosColor;
    document.getElementById("lineWeight").value = squadratinhosLineWeight;
  }
  countTiles();
});

function updateForm() {
  var bounds = map.getBounds();
  var northWest = bounds.getNorthWest();
  var southEast = bounds.getSouthEast();
	document.getElementById("NWlon").value = northWest.lng;
	document.getElementById("NWlat").value = northWest.lat;
	document.getElementById("SElon").value = southEast.lng;
	document.getElementById("SElat").value = southEast.lat;
	return;
}

function countTiles() {
  var bounds = map.getBounds();
  var northWest = bounds.getNorthWest();
  var southEast = bounds.getSouthEast();
	var tilesLon = lon2tile(southEast.lng,zoomLevel) - lon2tile(northWest.lng,zoomLevel);
	var tilesLat = lat2tile(southEast.lat,zoomLevel) - lat2tile(northWest.lat,zoomLevel);
	var tiles = tilesLon * tilesLat;
	document.getElementById("tilesNumber").innerHTML = tiles;
 	if (tiles > maxNumberOfSquadrats) {
		document.getElementById("submitButton").disabled = true;
	} else {
		document.getElementById("submitButton").disabled = false;
	}
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

<script src="aspect-ratio-chooser.js"></script>

</body>
</html>
