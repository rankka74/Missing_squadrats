<?php

require __DIR__ . '/functions.php';

if (empty($_GET['file'])) {
  die('Missing file argument');
}

$filename = basename(clean($_GET['file'])) . '.img';

if (file_exists(__DIR__ . '/img/' . $filename)) {
  header('Content-Description: File Transfer');
  header('Content-Type: application/octet-stream');
  header('Content-Disposition: attachment; filename="'.$filename.'"');
  header('Expires: 0');
  header('Cache-Control: must-revalidate');
  header('Pragma: public');
  header('Content-Length: ' . filesize($filename));
  readfile($filename);
  exit;
}
?>

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="10">
</head>
<body>
  <h1>Downloading <?php echo $filename; ?> ...</h1>
  <p>Please wait while the map is being generated. This may take up to 10 minutes.</p>.
</body>
</html>
