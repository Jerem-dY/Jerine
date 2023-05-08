<!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8">
    <title>JérIne</title>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
      <img src="images/JérIne.png" width="60%">
      <form method="POST" action="php/traitement.php">
          <h2>Créer un compte</h2>
          <label for="login">Login</label>
          <input type="login" id="login" name="login" required>
          <label for="Nom">Nom</label>
          <input type="Nom" id="Nom" name="Nom" required>
          <label for="Prénom">Prénom</label>
          <input type="Prénom" id="Prénom" name="Prénom" required>
          <label for="email">Adresse e-mail</label>
          <input type="email" id="email" name="email" required>
          <label for="password">Mot de passe</label>
          <input type="password" id="password" name="pwd" required>
          <label for="confirm-password">Confirmer le mot de passe</label>
          <input type="password" id="confirm-password" name="confirm-password" required>
          <button type="submit">Créer un compte</button>
      </form>

  </body>
</html>
