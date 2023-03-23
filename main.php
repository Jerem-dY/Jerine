<!doctype html>
<?php 


if(!(isset($_SESSION) && isset(_SESSION["id"]))){


    if(isset($_POST) && isset($_POST["login"]) && isset($_POST["pwd"])){

        include("php/connexion.php");

        $query = "SELECT user_id, password FROM `user` WHERE login='".$_POST["login"]."'" ;
    
        /* On exécute la requête : */
        if($response = $pdo->query($query)){

            if($record = $response->fetch()){
                $id = $record["user_id"];
                $pwd = $record["password"];

                if(password_verify($_POST["pwd"], $pwd)){
                    session_start();
                    $_SESSION["id"] = $id;
                    //echo "<br/>Session tokens set.<br/>";
                }
                else{
                    print "<br/>Authentification failed: wrong username or password. Aborting.<br/>";
                    header('Location: '."index.php?err=true");
                    die();                    
                }
                
            }
            else{
                print "<br/>Authentification failed: wrong username or password. Aborting.<br/>";
                header('Location: '."index.php?err=true");
                die();
            }
        
        }
        else{
            print "<br/>Couldn't get a response back from the database. Aborting.<br/>";
            header('Location: '."index.php");
            die();
        }
    }
    else{
        header('Location: '."index.php");
        die();
    }

    //echo "<br/>logged in.<br/>";
}

?>

<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Bourdillat-Adjoudj - espace de travail</title>
        <link rel="stylesheet" href="js/libs/jquery/jquery-ui/jquery-ui.css">
        <link rel="stylesheet" href="js/libs/jquery/DataTables/datatables.min.css"/>
        <link rel="stylesheet" href="css/style.css"/>
        <script type="text/javascript" src="js/libs/jquery/jquery-3.6.1.min.js"></script>
        <script type="text/javascript" src="js/libs/jquery/jquery-ui/jquery-ui.js"></script>
        <script type="text/javascript" src="js/libs/jquery/DataTables/datatables.min.js"></script>
        <script type="text/javascript" src="js/Overlay.js"></script>
    </head>
    <body>
        <button id="addFiles">Ajouter des documents</button>

        <table id="collection_content_table" class="refresh">
            <thead>
                <tr>
                    <th>Document</th>
                    <th>Phrases</th>
                    <th>Tokens</th>
                    <th>Lemmes</th>
                </tr>
            </thead>
        </table>

        <div id="documents_chart" style="height:400px;width:300px; "></div>

        <form action="./php/disconnect_session.php" method="get">
            <button id="disconnect">se déconnecter</button>
        </form>

    </body>
    <script type="text/javascript">

        let overlay = new Overlay("add_documents", $("body"));
    
        $( "#addFiles" ).button().on( "click", function() {
            overlay.show();
        });

        $( "#addFiles" ).button("option", "icon", "ui-icon-document");

        $("#disconnect").button();


        $('#collection_content_table').DataTable({
            'processing': true,
            'serverSide': true,
            select: true,
            'serverMethod': 'post',
            dataSrc: 'aaData',
            'ajax': {
                'url':'php/getCollectionContent.php'
            },
            'columns': [	
                { data: 'document_name' },
                { data: 'sents' },
                { data: 'tokens' },
                { data: 'lemmas' }
            ]
        });


        $(".refresh").on("refresh_tables", function(event){
            $('.refresh').DataTable().ajax.reload();
        })



    </script>
</html>