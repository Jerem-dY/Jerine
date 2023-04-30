<?php 

include ('connexion.php');
include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$user_id = $_SESSION["user_id"];

$query = "SELECT document.document_id as id, document.document_name as name FROM document
INNER JOIN collection_has_document ON collection_has_document.document_id = document.document_id
INNER JOIN user ON user.documents = collection_has_document.collection_id
WHERE user.user_id = $user_id;";

$data = array();

if($response = $pdo->query($query)){

    while($record = $response->fetch()){
        $data[] = array(
            "id" => $record["id"],
            "name" => $record["name"]
        );
    }
}
else{
    print "<br/>Failed to execute query. Aborting.<br/>";
    http_response_code(500);
    exit;
}


header("Content-Type: application/json; charset=utf-8");
echo json_encode($data);
http_response_code(200);
exit;

?>