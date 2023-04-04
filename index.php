<?php 

include("php/start_session.php");

if(isset($_SESSION) && isset($_SESSION["user_id"])){
	header('Location: '."main.php");
    die();
}

?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="js/libs/jquery/jquery-ui/jquery-ui.css">
    <link rel="stylesheet" href="css/style2.css">
    <script type="text/javascript" src="js/libs/jquery/jquery-3.6.1.min.js"></script>
    <script type="text/javascript" src="js/libs/jquery/jquery-ui/jquery-ui.js"></script>
    <title>JérIne</title>
    
  </head>
  <body>

    <?php 
    if(isset($_GET["err"])){
        echo "<p class=\"ui-state-error\">Nom d'utilisateur ou mot de passe erroné !</p>";
    }
    ?>

    <img src="C:\Users\djaam\Downloads\JérIne.png"? width="60%">

    <form action="page_de_connexion.html" method="post">

      <label for="email">Adresse e-mail :</label>
      <input type="email" id="email" name="email" required>

      <label for="password">Mot de passe :</label>
      <input type="password" id="password" name="password" required>

      <button type="submit">Se connecter</button>
      
    </form>

    <form id="creer_compte" action="creation_de_compte.html"> <button type="submit"> Créer un compte </button> </form>
    <a href="docs/index.html">Documentation du projet</a> 
    
  </body>
</html>


