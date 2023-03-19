<?php


try{
    $pdo = new PDO('mysql:host=localhost;dbname=bourdillat', 'bourdillat', 'Uibbnqkbavs09//');
    print "La base est ouverte !<br/>\n";
}
catch(Exception $e){
    die('Erreur : '.$e->getMessage());
    print "Accès impossible à la base !<br/>\n";
}


?>