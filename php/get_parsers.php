<?php


include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$cmd = "/home/IdL/2022/bourdillat/miniconda3/envs/website/bin/python3.9 ../python/generate_parsers.py 2>&1";
$process_out = exec($cmd, $return);

echo $return[0];

?>