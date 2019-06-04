<?php
require_once("config.php");

function get_entry($title){
    $curl = curl_init();
    $options = array(
        CURLOPT_URL => "http://" . API_SERVER_NAME . ":" . (string)API_SERVER_PORT . "?" . http_build_query(array("title" => $title)),
        CURLOPT_CUSTOMREQUEST => "GET",
        CURLOPT_RETURNTRANSFER => true
    );
    curl_setopt_array($curl, $options);
    $source = curl_exec($curl);
    curl_close($curl);
    return json_decode($source, true);
}

$json = get_entry(null);
?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <title>Entry Checker</title>
  <link rel="stylesheet" href="css/index.css" type="text/css" />
</head>
<body>
  <article>
    <h1><?php echo $json["title"]; ?></h1>
    <table>
      <tbody>
        <tr>
          <td><?php echo htmlspecialchars($json["content"]); ?></td>
          <td><?php echo htmlspecialchars($json["sentences"]); ?></td>
        </tr>
      </tbody>
    </table>
  </article>
</body>
</html>
