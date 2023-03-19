<?php 

include("connexion.php");


/**
 * Etape 1 : on vérifie que l'on a bien toutes les infos nécesaires, puis on récupère l'id de l'utilisateur.
 *  
 * */
if(isset($_POST) && isset($_POST['username']) && isset($_POST['password'])){
    print_r($_POST);

    $query = "SELECT id FROM `user` WHERE password='".$_POST['password']."' AND login='".$_POST['username']."'" ;
    
    /* On exécute la requête : */
    if($response = $pdo->query($query)){

        if($record = $response->fetch()){
            $id = $record["id"];
        }
        else{
            print "<br/>Authentification failed: wrong username or password. Aborting.<br/>";
            http_response_code(401);
            exit;
        }
    
    }
    else{
        print "<br/>Couldn't get a response back from the database. Aborting.<br/>";
        http_response_code(500);
        exit;
    }
    
}
else{
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}


/**
 * Etape 2 : on crée le dossier qui va accueillir les fichiers à traiter, s'il n'existe pas déjà.
 *  
 * */
$uploads_path = getcwd().DIRECTORY_SEPARATOR."..".DIRECTORY_SEPARATOR."uploads".DIRECTORY_SEPARATOR.$id.DIRECTORY_SEPARATOR;

if(is_dir($uploads_path)){

    if(!is_writable($uploads_path)){
        print "<br/>Upload dir #".$id." is not writeable. Aborting.<br/>";
        http_response_code(500);
        exit;
    }
}else{
    if(!mkdir($uploads_path, 0777)){
        print "<br/>Couldn't make the directory #".$id." for upload : '".$uploads_path."'. Aborting.<br/>";
        http_response_code(500);
    exit;
    }
}


/**
 * Etape 3 : on vérifie les fichiers à uploader.
 *  
 * */
if(!isset($_FILES)){
    print "<br/>No files to upload. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$size = 0;
foreach ($_FILES as $file) {
    $size += $file['size'];
}

if($size > 1000000){
    print "<br/>Upload size is too big : ".$size.". Aborting.<br/>";
    http_response_code(400);
    exit;
}


/**
 * Etape 4 : on upload les fichiers à traiter.
 *  
 * */
$to_delete = array();

foreach ($_FILES as $file) {

    $target_path = $uploads_path.basename($file['name']);

    if (move_uploaded_file($file['tmp_name'], $target_path)) {
        array_push($to_delete, $target_path);
        chmod($target_path, 0777);
        echo "<br/>File '".$file['name']."' is valid, and was successfully uploaded at '".$target_path."'.<br/>";
    } else {
        echo "<br/>Possible file upload attack! File '".$file['name']."' not uploaded.<br/>";
    }
}

echo "<br/>Files tranferred.<br/>";

/**
 * Etape 5 : On traite les fichiers.
 *  
 * */

// .......................


/**
 * Etape 6 : on supprime les fichier temporaires du serveur.
 *  
 * */

 foreach($to_delete as $del_file){

    if(!is_file($del_file)){
        echo "<br/>Something went wrong...<br/>";
    }

    if(!unlink($del_file)){
        echo "<br/>Couldn't delete file '".$del_file."'!<br/>";
    }
 }

http_response_code(200);
exit;
?>