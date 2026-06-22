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
