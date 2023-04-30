<?php 

include ('connexion.php');
include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_POST["document_ids"]) && isset($_POST["collection_id"]))){

    echo "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$collection_id = $_POST['collection_id'];
$document_ids = json_decode($_POST["document_ids"], true);

$query = "INSERT INTO collection_has_document
(collection_id, document_id) VALUES ($collection_id, ";

foreach ($document_ids as $id) {

    if(!($response = $pdo->query($query.$id.");"))){
        echo "Query: ".$query.$id.");";
        echo $response;
        http_response_code(500);
        exit;
    }

}


http_response_code(200);
exit;


?>