<!doctype html>
<?php 

include("php/start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]))){


    if(isset($_POST) && isset($_POST["login"]) && isset($_POST["pwd"])){

        include("php/connexion.php");

        $query = "SELECT user_id, password FROM `user` WHERE login='".$_POST["login"]."'" ;
    
        /* On exécute la requête : */
        if($response = $pdo->query($query)){

            if($record = $response->fetch()){
                $id = $record["user_id"];
                $pwd = $record["password"];

                if(password_verify($_POST["pwd"], $pwd)){
                    $_SESSION["user_id"] = $id;
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
        <link rel="icon" type="image/x-icon" href="icon.png">
        <link rel="stylesheet" href="js/libs/jquery/jquery-ui/jquery-ui.css">
        <link rel="stylesheet" href="js/libs/jquery/DataTables/datatables.min.css"/>
        <link rel="stylesheet" href="js/libs/jquery/jsTree/themes/default/style.min.css"/>
        <link rel="stylesheet" href="css/style.css"/>
        <script type="text/javascript" src="js/libs/jquery/jquery-3.6.1.min.js"></script>
        <script type="text/javascript" src="js/libs/jquery/jquery-ui/jquery-ui.js"></script>
        <script type="text/javascript" src="js/libs/jquery/DataTables/datatables.min.js"></script>
        <script type="text/javascript" src="js/libs/jquery/jsTree/jstree.min.js"></script>
        <script type="text/javascript" src="js/Overlay.js"></script>
        <script type="text/javascript" src="js/DataTab.js"></script>
        <script type="text/javascript" src="js/TabManager.js"></script>
        <script type="text/javascript" src="js/LeftPannel.js"></script>
        <script type="text/javascript" src="js/RightPannel.js"></script>
    </head>
    <body>
        <div class="fg">
            <div id="topbar" class="ui-corner-all ui-widget">
                <form action="./php/disconnect_session.php" method="get">
                    <button id="disconnect">se déconnecter</button>
                </form>
            </div>
            <div id="mainarea">

            </div>
        </div>

    </body>
    <script type="text/javascript">


        let leftpannel = new LeftPannel("leftpannel", $("#mainarea"));
        let tabmanager;
        let rightpannel;
        
        leftpannel.tree.on('ready.jstree', function (e, data) {
            tabmanager = new TabManager("tabmanager", $("#mainarea"));
            rightpannel = new RightPannel("rightpannel", $("#mainarea"));

            $(document).on("refresh_tables", ".refresh", function(event){
                //$('.refreshtree').jstree(true).refresh();    
                $('.refreshtable').DataTable().ajax.url('php/get_collection_content.php?collection_id='+$("#collectiontree").jstree("get_selected", true)[0].original.collection_id);
                $('.refreshtable').DataTable().ajax.reload();    
            });
        });

        

        $("#disconnect").button();


        



    </script>
</html>