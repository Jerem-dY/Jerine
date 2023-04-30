<?php

include("env.php");

putenv("LC_ALL=en_US.UTF-8");

try{
    $pdo = new PDO(...$DB_CONFIG);
    //print "La base est ouverte !<br/>\n";
}
catch(Exception $e){
    die('Erreur : '.$e->getMessage());
    print "Accès impossible à la base !<br/>\n";
}

?>