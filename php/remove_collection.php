<?php

include ('connexion.php');
include("start_session.php");


if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_POST["collection_id"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$cid = $_POST["collection_id"];
$id = $_SESSION["user_id"];

$query = 
"DELETE FROM user_has_collection WHERE user_has_collection.user_id = $id AND user_has_collection.collection_id = $cid ;";

if(!($response = $pdo->query($query))){
    echo "<br/>Failed to remove the collection '".$_POST["collection_name"]."' for user '".$_SESSION["user_id"]."'. Aborting.<br/>";
    http_response_code(500);
    exit;
}

http_response_code(200);
exit;

?>