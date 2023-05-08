<?php
include("connexion.php");


if(!(isset($_POST) && isset($_POST["login"]) && isset($_POST["email"]) && isset($_POST["pwd"]) && isset($_POST["confirm-password"]) && isset($_POST["Prénom"]) && isset($_POST["Nom"])))
{
    echo "<br/>required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    die();
}

if($_POST["confirm-password"] != $_POST["pwd"] || $_POST["pwd"] == ""){
    echo "<br/>Token mismatch for password. Aborting.<br/>";
    http_response_code(400);
    die();
}


// récupérer les données du formulaire
$login = $_POST["login"];
$email = $_POST["email"];
$pwd = password_hash($_POST["pwd"], PASSWORD_DEFAULT);
$fname = $_POST["Prénom"];
$surname = $_POST["Nom"];

// Réception et validation des identifiants 
$sql = "SELECT * FROM user WHERE login ='$login'";
$result = $pdo->query($sql);

if ($result->rowCount() == 0) {
    // Les identifiants sont valides
    echo "Bienvenue, ".$login." !";
} else {
    // Les identifiants sont invalides
    echo "Identifiants incorrects.";
    http_response_code(400);
    die();
}

// préparer une requête SQL pour insérer les données dans la base de données
$stmt = $pdo->prepare("INSERT INTO user (login, password, email, fname, surname) VALUES (:login, :pwd, :email, :fname, :surname)");

// lier les paramètres de la requête à leurs valeurs respectives
$stmt->bindParam(':login', $login);
$stmt->bindParam(':email', $email);
$stmt->bindParam(':pwd', $pwd);
$stmt->bindParam(':fname', $fname);
$stmt->bindParam(':surname', $surname);

// exécuter la requête
if ($stmt->execute()) {
    echo "Compte créé avec succès";
} else {
    echo "Erreur lors de la création du compte";
}

// Fermer la connexion à la base de données
$pdo = null;
?>
