<?php

$jsonString = '{"name":"Joe","age":42,"scores":[31.4,29.9,35.7],"winner":false}';

// deserialize: parse text into a JSON object
// note: use json_decode($text, true) to parse into an array instead of object
$json = json_decode($jsonString, true);
echo $json['name'];
echo "\n";

$json['winner'] = true;

$stringified = json_encode($json);
var_dump($stringified);

?>
