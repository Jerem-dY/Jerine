<?php


include("start_session.php");
include("env.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$cmd = $PYTHON_PATH." ../python/generate_parsers.py 2>&1";
$process_out = exec($cmd, $return);

echo $return[0];

?>