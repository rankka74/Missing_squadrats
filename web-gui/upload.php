<?php

function clean($string) {
   $string = str_replace(' ', '_', $string); // Replaces all spaces with hyphens.

   return preg_replace('/[^A-Za-z0-9\-]/', '', $string); // Removes special chars.
}

function is_valid_squadrats_kml($file): bool {
  libxml_use_internal_errors(true);

  $dom = new \DOMDocument();
  if (!$dom->load($file)) {
    return FALSE;
  }

  // Search for Kml->Document->Placemark elements.
  $placemarks = $dom->getElementsByTagName('kml')->item(0)
    ?->getElementsByTagName('Document')->item(0)
    ?->getElementsByTagName('Placemark');

  if (!$placemarks->length > 0) {
    return FALSE;
  }

  // Search for Placemark->name element with the value of "squadrats".
  foreach ($placemarks as $placemark) {
    $name = $placemark->getElementsByTagName('name')->item(0)?->textContent;

    if ($name === 'squadrats') {
      return TRUE;
    }
  }
  return FALSE;
}

$tmpName = $_FILES['fileToUpload']['tmp_name'] ?? NULL;

if (empty($tmpName) || !is_valid_squadrats_kml($tmpName)) {
  die("Invalid .kml file.");
}
$cookie_name = "MissingSquadrats";
$userName = clean($_POST['name']);
$NWlon = (float) $_POST['NWlon'] ?? 0;
$NWlat = (float) $_POST['NWlat'] ?? 0;
$SElon = (float) $_POST['SElon'] ?? 0;
$SElat = (float) $_POST['SElat'] ?? 0;
$lineWeight = (int) $_POST['lineWeight'] ?? 5;
$lineColor = str_replace("#", "", clean($_POST['lineColor'] ?? '5853A3A'));
$zoomLevel = (int) $_POST['zoomLevel'] ?? 14;
$target_dir = "../../jobs/missing_squadrats/";
$fileName = date('Y-m-d') . '-' . $userName;

if (!ctype_xdigit($lineColor)) {
  die('Invalid lineColor');
}

if ($lineWeight < 1 || $lineWeight > 10) {
  die('Invalid lineWeight. Must be 1-10');
}

if (!in_array($zoomLevel, [14, 17])) {
  die('Invalid zoomLevel. Must be 14 or 17.');
}

if (!$NWlon || !$NWlat || !$SElon || !$SElat) {
  die('Invalid coordinates.');
}

# echo "Name: " . $userName . "<BR>\r\n";
if (!empty($_POST['cookie'])) {
  $cookieValues = [
    "mapCenterLat" => $SElat + (($NWlat - $SElat) / 2),
    "mapCenterLon" => $SElon + (($NWlon - $SElon) / 2),
    "zoomLevel" => $zoomLevel,
    "squadratinhosLineWeight" => $lineWeight,
    "squadratinhosColor" => "#$lineColor",
    "squadratsLineWeight" => $lineWeight,
    "squadratsColor" =>  "#$lineColor",
  ];

  if (isset($_COOKIE[$cookie_name])) {
    $previousValues = json_decode($_COOKIE[$cookie_name], true);
    // Never override the color or weight for opposite zoom level.
    $selector = $zoomLevel === 14 ? "squadratinhos" : "squadrats";

    foreach (["{$selector}Color", "{$selector}LineWeight"] as $key) {
      if (!isset($previousValues[$key])) {
        continue;
      }
      $cookieValues[$key] = $previousValues[$key];
    }
  }

  setcookie("MissingSquadrats", json_encode($cookieValues), time() + (86400 * 30)); // 86400 = 1 day
}

?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body>

<h1>Upload a kml file</h1>

<p>Everything ok. Please go back to the main page</p><br>

<?php

#echo "OSM file name: " . $target_file . "<BR>\r\n";
if (move_uploaded_file($tmpName, $target_dir . $fileName . '.kml')) {
	echo "The file ". $fileName . " has been uploaded.<BR>\r\n";
} else {
		echo "Sorry, there was an error uploading your file.<BR>\r\n";
    exit;
}

$job = implode(',', [
  'filename' => $fileName,
  'username' => $userName,
  'nwlon' => $NWlon,
  'nwlat' => $NWlat,
  'selon' => $SElon,
  'selat' => $SElat,
  'lineWeight' => $lineWeight,
  'lineColor' => $lineColor,
  'zoomLevel' => $zoomLevel,
]);
file_put_contents($target_dir . $fileName . '.csv', $job);

// In Docker: spawn Python directly so cron is not needed for local development.
if (file_exists('/.dockerenv')) {
  echo "Processing map, please wait...<BR>\r\n";
  flush();

  set_time_limit(0);

  $args = [
    '/usr/bin/python3',
    '/srv/src/missing_squadrats/missing_squadrats.py',
    $fileName . '.kml',
    $userName,
    (string) $NWlon,
    (string) $NWlat,
    (string) $SElon,
    (string) $SElat,
    (string) $squadratinhosLineWeight,
    $squadratinhosColor,
  ];
  $descriptors = [
    0 => ['pipe', 'r'],
    1 => ['file', '/home/users/oranta/missingSquadrats.log', 'a'],
    2 => ['file', '/home/users/oranta/missingSquadrats.log', 'a'],
  ];
  $proc = proc_open($args, $descriptors, $pipes, '/srv/src/missing_squadrats');
  if (is_resource($proc)) {
    fclose($pipes[0]);
    $exitCode = proc_close($proc);
    if ($exitCode === 0) {
      echo "Done! <a href=\"index.php\">Go back</a> to download your map.<br>\r\n";
    } else {
      echo "Processing failed (exit code $exitCode). Check the log for details.<br>\r\n";
    }
  } else {
    echo "Failed to start processing.<br>\r\n";
  }
}
?>

</body>
</html>
