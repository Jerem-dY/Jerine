<?php 

include("connexion.php");
session_start();

/**
 * Etape 1 : on vérifie que l'on a bien toutes les infos nécesaires, puis on récupère l'id de l'utilisateur.
 *  
 * */
if(!(isset($_SESSION) && isset($_SESSION["id"]))){

    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}


/**
 * Etape 2 : on crée le dossier qui va accueillir les fichiers à traiter, s'il n'existe pas déjà.
 *  
 * */
$uploads_path = getcwd().DIRECTORY_SEPARATOR."..".DIRECTORY_SEPARATOR."uploads".DIRECTORY_SEPARATOR.$_SESSION["id"].DIRECTORY_SEPARATOR;

if(is_dir($uploads_path)){

    if(!is_writable($uploads_path)){
        print "<br/>Upload dir #".$_SESSION["id"]." is not writeable. Aborting.<br/>";
        http_response_code(500);
        exit;
    }
}else{
    if(!mkdir($uploads_path, 0777)){
        print "<br/>Couldn't make the directory #".$_SESSION["id"]." for upload : '".$uploads_path."'. Aborting.<br/>";
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


//putenv("LC_ALL=en_US.UTF-8");

//echo exec("/home/IdL/2022/bourdillat/miniconda3/bin/conda init 2>&1", $return);
//echo exec("/home/IdL/2022/bourdillat/miniconda3/bin/conda activate website 2>&1", $return);

//print_r($return);

$cmd = "/home/IdL/2022/bourdillat/miniconda3/envs/website/bin/python3.9 ../python/inputdata.py";

foreach($to_delete as $f){
    $cmd = $cmd." '".$f."'";
}

$cmd = $cmd." "."-u ".$_SESSION["id"]." 2>&1";

$process_out = exec($cmd, $return);
print_r($return);


if($process_out != 0){
    http_response_code(500);
    echo("<br/>Something went wrong while processing the files!<br/>");
}
else{
    http_response_code(200);
    echo("Fichiers traités.");
}



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

exit;
?>