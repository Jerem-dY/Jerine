<?php 

include("connexion.php");
include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_POST["document_ids"]) && isset($_POST["collection_id"]))){

    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$collection_id = $_POST['collection_id'];
$document_ids = json_decode($_POST["document_ids"], true);

/* Construction de la requête */
//TODO: valider les données d'entrée pour éviter les injections
$query = "DELETE FROM collection_has_document
WHERE collection_id = $collection_id AND (0";
foreach($document_ids as $doc_id){
    $query = $query." OR document_id = ".$doc_id;
}

$query = $query.");";

if(!($response = $pdo->query($query))){
    echo "Query: ".$query;
    echo $response;
    http_response_code(500);
    exit;
}


http_response_code(200);
exit;


?>