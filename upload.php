<!DOCTYPE html>

<?php
# https://www.w3schools.com/PHP/php_file_upload.asp

# echo "Overwrite:" . $_POST['overwrite'] . "<BR>\r\n";

$tmpName = $_FILES['fileToUpload']['tmp_name'];
# $kmlFileName = htmlspecialchars( basename( $_FILES['fileToUpload']['name']));
$kmlFileName = clean( basename( $_FILES['fileToUpload']['name']));
$userName = $_POST['name'];
$NWlon = $_POST['NWlon'];
$NWlat = $_POST['NWlat'];
$SElon = $_POST['SElon'];
$SElat = $_POST['SElat'];
$saveCookie = $_POST['cookie'];
$target_dir = "../../jobs/missing_squadrats/";

# echo "Name: " . $userName . "<BR>\r\n";

if ($saveCookie == true) {
  # $mapCenter = array("latCenter"=>61.24, "lonCenter"=>24.90);
  $mapCenter = array("latCenter"=>$SElat + (($NWlat - $SElat) / 2), "lonCenter"=>$SElon + (($NWlon - $SElon) / 2));
  # https://www.w3schools.com/php/php_cookies.asp
  # https://stackoverflow.com/questions/32567709/how-to-store-raw-json-string-in-cookie-with-php
  setcookie("MissingSquadrats", json_encode($mapCenter), time() + (86400 * 30)); // 86400 = 1 day
}

# https://stackoverflow.com/questions/14114411/remove-characters-that-arent-letters-and-numbers-replace-space-with-a-hyphen
function clean($string) {
   $string = str_replace(' ', '-', $string); // Replaces all spaces with hyphens.

   return preg_replace('/[^A-Za-z0-9\-\.]/', '', $string); // Removes special chars.
}
?>

<html>
<body>

<h1>Upload a kml file</h1>

<p>Everything ok. Please go back to the main page<br>

<?php

# https://www.w3schools.com/php/php_file_upload.asp
$target_file = $target_dir . str_replace(".kml", "-" . $userName . ".kml", $kmlFileName);
#echo "OSM file name: " . $target_file . "<BR>\r\n";

if (move_uploaded_file($tmpName, $target_file)) {
	echo "The file ". $target_file . " has been uploaded.<BR>\r\n";
} else {
		echo "Sorry, there was an error uploading your file.<BR>\r\n";
		$uploadOk = 0;
}

$kmlFileNameName = str_replace(".kml", "-" . $userName . ".kml", $kmlFileName);
#echo "KML file name name: " . $kmlFileNameName . "<BR>\r\n";
$command = "python3 /var/www/10/oranta/sites/oranta.kapsi.fi/src/missing_squadrats/missing_squadrats.py $kmlFileNameName $userName $NWlon $NWlat $SElon $SElat >> /home/users/oranta/missingSquadrats.log 2>&1";


#$output = exec("export PYTHONPATH=/home/users/oranta/.local/lib/python3.9/site-packages && python3 ../../src/missing_squadrats/missing_squadrats.py", $target_file, "2>&1", $out, $status);
#$output = shell_exec($command);
#echo $output . "<BR>\r\n";

$shFileName = str_replace(".kml", "-" . $userName . ".sh", $kmlFileName);
$myfile = fopen($shFileName, "w") or die("Unable to open file!");
fwrite($myfile, "#!/usr/bin/bash\r\n");
fwrite($myfile, $command);
fclose($myfile);
rename($shFileName, "../../jobs/missing_squadrats/" . $shFileName);
if (chmod("../../jobs/missing_squadrats/" . $shFileName, 0755)) {
	#echo "Run script permissions ok.<BR>\r\n";
} else {
	#echo "Sorry, there was a problem with run script permissions.<BR>\r\n";
	$uploadOk = 0;
}

# $command = "sh ../../jobs/missing_squadrats/" . $shFileName;

# $logFilePath = "/home/10/oranta/missingSquadrats.log";
# $toLog = date("%Y.%m.%d %H:%i:%s");
# $myfile = file_put_contents($logFilePath, $toLog.PHP_EOL , FILE_APPEND | LOCK_EX);

exec($command);

# echo "<BR>\r\n<A href=\"img/veloviewer-" . date('Ymd') . "-" . $userName . ".img\">" . "veloviewer-" . date('Ymd') . "-" . $userName . ".img" . "</A><BR>\r\n"
?>

</body>
</html>
