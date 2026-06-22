<?php

require __DIR__ . '/functions.php';

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
$lineWeight = (int) $_POST['lineWeight'] ?? 0;
$lineColor = str_replace("#", "", clean($_POST['lineColor']));
$zoomLevel = (int) $_POST['zoomLevel'] ?? 0;
$target_dir = "../../jobs/missing_squadrats/";
$fileName = date('Y-m-d') . '-' . $userName;

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

if (!move_uploaded_file($tmpName, $target_dir . $fileName . '.kml')) {
  die("Sorry, there was an error uploading your file.");
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

if (!file_put_contents($target_dir . $fileName . '.csv', $job)) {
  die("Sorry, there was an error uploading your file.");
}

header('Location: file.php?file=' . $fileName);
exit;
