<?php 

include("connexion.php");
include("start_session.php");



$normalizeChars = array(
    'Š'=>'S', 'š'=>'s', 'Ð'=>'Dj','Ž'=>'Z', 'ž'=>'z', 'À'=>'A', 'Á'=>'A', 'Â'=>'A', 'Ã'=>'A', 'Ä'=>'A',
    'Å'=>'A', 'Æ'=>'A', 'Ç'=>'C', 'È'=>'E', 'É'=>'E', 'Ê'=>'E', 'Ë'=>'E', 'Ì'=>'I', 'Í'=>'I', 'Î'=>'I',
    'Ï'=>'I', 'Ñ'=>'N', 'Ń'=>'N', 'Ò'=>'O', 'Ó'=>'O', 'Ô'=>'O', 'Õ'=>'O', 'Ö'=>'O', 'Ø'=>'O', 'Ù'=>'U', 'Ú'=>'U',
    'Û'=>'U', 'Ü'=>'U', 'Ý'=>'Y', 'Þ'=>'B', 'ß'=>'Ss','à'=>'a', 'á'=>'a', 'â'=>'a', 'ã'=>'a', 'ä'=>'a',
    'å'=>'a', 'æ'=>'a', 'ç'=>'c', 'è'=>'e', 'é'=>'e', 'ê'=>'e', 'ë'=>'e', 'ì'=>'i', 'í'=>'i', 'î'=>'i',
    'ï'=>'i', 'ð'=>'o', 'ñ'=>'n', 'ń'=>'n', 'ò'=>'o', 'ó'=>'o', 'ô'=>'o', 'õ'=>'o', 'ö'=>'o', 'ø'=>'o', 'ù'=>'u',
    'ú'=>'u', 'û'=>'u', 'ü'=>'u', 'ý'=>'y', 'ý'=>'y', 'þ'=>'b', 'ÿ'=>'y', 'ƒ'=>'f',
    'ă'=>'a', 'î'=>'i', 'â'=>'a', 'ș'=>'s', 'ț'=>'t', 'Ă'=>'A', 'Î'=>'I', 'Â'=>'A', 'Ș'=>'S', 'Ț'=>'T', 
    ' '=>'_', '\t'=>'__',
);



/**
 * Etape 1 : on vérifie que l'on a bien toutes les infos nécesaires.
 *  
 * */
if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_POST["processors"]) && isset($_POST["types"]))){

    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

$processors = json_decode($_POST["processors"], true);
$types = json_decode($_POST["types"], true);

/**
 * Etape 2 : on crée le dossier qui va accueillir les fichiers à traiter, s'il n'existe pas déjà.
 *  
 * */
$uploads_path = getcwd().DIRECTORY_SEPARATOR."..".DIRECTORY_SEPARATOR."uploads".DIRECTORY_SEPARATOR.$_SESSION["user_id"].DIRECTORY_SEPARATOR;

if(is_dir($uploads_path)){

    if(!is_writable($uploads_path)){
        print "<br/>Upload dir #".$_SESSION["user_id"]." is not writeable. Aborting.<br/>";
        http_response_code(500);
        exit;
    }
}else{
    if(!mkdir($uploads_path, 0777)){
        print "<br/>Couldn't make the directory #".$_SESSION["user_id"]." for upload : '".$uploads_path."'. Aborting.<br/>";
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

 // Volé ici : https://stackoverflow.com/questions/46842606/how-to-convert-a-file-to-utf-8-in-php
 function convert_to_utf8($source) {

    $content=file_get_contents($source);
    # detect original encoding
    $original_encoding=mb_detect_encoding($content, null, true);
    # now convert
    if ($original_encoding!='UTF-8') {
        $content=mb_convert_encoding($content, 'UTF-8', $original_encoding);
        echo "<br/>Fichier '".$file['name']."' converti en utf-8.<br/>";
    }
    $bom=chr(239) . chr(187) . chr(191); # use BOM to be on safe side
    file_put_contents($source, $bom.$content);
}

$to_delete = array();

foreach ($_FILES as $file) {

    $target_path = $uploads_path.basename(strtr($file['name'], $normalizeChars));

    if (move_uploaded_file($file['tmp_name'], $target_path)) {
        array_push($to_delete, $target_path);
        //chmod($target_path, 0777);
        convert_to_utf8($target_path);
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

$cmd = $cmd." "."-u ".$_SESSION["user_id"]." -p ".$processors["tokenizer"]." ".$processors["tagger"]." ".$processors["lemmatizer"]." ".$processors["dependency_analyzer"]." -t ";

foreach($types as $t){
    $cmd = $cmd.$t." ";
}


$cmd = $cmd."2>&1";

$process_out = exec($cmd, $return);

foreach($return as $line){
    echo $line."<br/>";
}


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