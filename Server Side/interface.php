<?php

$data = file_get_contents("php://input");
$json = json_decode($data);

$output = shell_exec("python analyze.py \"".($json->text)."\" 2>&1");

echo $output

?>
