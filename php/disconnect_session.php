<?php 

include("start_session.php");

session_unset();
session_destroy();

header('Location: '."../index.php");
die();


?>