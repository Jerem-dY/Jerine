<?php

include ('connexion.php');
include("start_session.php");


if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_POST["collection_name"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$name = $_POST["collection_name"];
$id = $_SESSION["user_id"];

$query = "INSERT INTO collection (collection_name, is_main) VALUES ('$name', 0);
INSERT INTO user_has_collection (user_id, collection_id) VALUES ($id, LAST_INSERT_ID());";

echo $query;

if(!($response = $pdo->query($query))){
    echo "<br/>Failed to insert the collection '".$_POST["collection_name"]."' for user '".$_SESSION["user_id"]."'. Aborting.<br/>";
    echo $response;
    http_response_code(500);
    exit;
}


http_response_code(200);
exit;

?>