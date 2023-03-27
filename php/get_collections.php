<?php



include ('connexion.php');
include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}


$json = array();

/* On commence par la collection principale, celle réservée à l'utilisateur : */
$query = "select user.documents from user where user.user_id = ".$_SESSION["user_id"];

if(!($response = $pdo->query($query))){
    echo "<br/>Failed to fetch user collections. Aborting.<br/>";
    http_response_code(500);
    exit;
}

while($record = $response->fetch()){
    array_push($json, array(
        "parent" => "#",
        "id" => "mes_documents",
        "text" => "Mes documents",
        "icon" => "jstree-file",
        "state" => array(
            "opened" => true,
            "disabled" => false,
            "selected" => true
        ),
        "collection_id" => $record["documents"]

    ));
}

/* On fait ensuite les collections créées par l'utilisateur : */
$query = "SELECT collection_name as name, collection.collection_id as id FROM collection
JOIN user_has_collection ON user_has_collection.collection_id = collection.collection_id
WHERE user_has_collection.user_id = ".$_SESSION["user_id"];

if(!($response = $pdo->query($query))){
    echo "<br/>Failed to fetch user collections. Aborting.<br/>";
    http_response_code(500);
    exit;
}

while($record = $response->fetch()){
    array_push($json, array(
        "parent" => "mes_documents",
        "id" => $record["name"],
        "text" => $record["name"],
        "icon" => "jstree-folder",
        "state" => array(
            "opened" => true,
            "disabled" => false,
            "selected" => false
        ),
        "collection_id" => $record["id"]

    ));
}

header('Content-type: text/json');
header('Content-type: application/json');
header('Access-Control-Allow-Origin: *');
echo json_encode($json);


?>