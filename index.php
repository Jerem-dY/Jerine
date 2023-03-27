<!doctype html>
<?php 

include("php/start_session.php");

if(isset($_SESSION) && isset($_SESSION["user_id"])){
	header('Location: '."main.php");
    die();
}

?>

<html lang="fr">
	<head>
		<meta charset="utf-8">
        <link rel="stylesheet" href="js/libs/jquery/jquery-ui/jquery-ui.css">
		<link rel="stylesheet" href="css/style.css"/>
		<link rel="icon" type="image/x-icon" href="icon.png">
        <script type="text/javascript" src="js/libs/jquery/jquery-3.6.1.min.js"></script>
        <script type="text/javascript" src="js/libs/jquery/jquery-ui/jquery-ui.js"></script>
        <title>Bourdillat-Adjoudj</title>
	</head>

	<body>

	<div class="fg">
		<?php 
            if(isset($_GET["err"])){
                echo "<p class=\"ui-state-error\">Nom d'utilisateur ou mot de passe erroné !</p>";
            }
        ?>
		
		<form action="main.php" method="post">
			<input type="text" name="login">
			<input type="text" name="pwd">
			<input type="submit">
		</form>
		<a href="docs/index.html">Documentation du projet</a> 
	</div>
	</body>

</html>