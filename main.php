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
        <link rel="root" href="./"/>
        <link rel="stylesheet" href="js/libs/jquery/jquery-ui/jquery-ui.css">
        <link rel="stylesheet" href="js/libs/jquery/DataTables/datatables.min.css"/>
        <link rel="stylesheet" href="js/libs/jquery/jsTree/themes/default/style.min.css"/>
        <link rel="stylesheet" href="css/style.css"/>
        <link rel="stylesheet" href="js/libs/annodoc/css/main.css">
		<link rel="stylesheet" href="js/libs/annodoc/css/style-vis.css">

        <script type="text/javascript" src="js/libs/jquery/jquery-3.6.1.min.js"></script>
        <script type="text/javascript" src="js/libs/jquery/jquery-ui/jquery-ui.js"></script>
        <script type="text/javascript" src="js/libs/jquery/DataTables/datatables.min.js"></script>
        <script type="text/javascript" src="js/libs/jquery/jsTree/jstree.min.js"></script>
        <script type="text/javascript" src="js/Overlay.js"></script>
        <script type="text/javascript" src="js/ViewTab.js"></script>
        <script type="text/javascript" src="js/DataTab.js"></script>
        <script type="text/javascript" src="js/TabManager.js"></script>
        <script type="text/javascript" src="js/LeftPannel.js"></script>
        <script type="text/javascript" src="js/RightPannel.js"></script>



		<!-- head.js, required for embedding -->
		<script type="text/javascript" src="js/libs/annodoc/lib/ext/head.load.min.js"></script>
        
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

        var root = './js/libs/annodoc/'; // filled in by jekyll
        head.js(
        // External libraries
        root + 'lib/ext/jquery.svg.min.js',
        root + 'lib/ext/waypoints.min.js',
        // brat helper modules
        root + 'lib/brat/configuration.js',
        root + 'lib/brat/util.js',
        root + 'lib/brat/annotation_log.js',
        root + 'lib/ext/webfont.js',
        // brat main modules
        root + 'lib/brat/dispatcher.js',
        root + 'lib/brat/url_monitor.js',
        root + 'lib/brat/visualizer.js',
        // external parsing libraries
        root + 'lib/ext/conllu.js/conllu.js',
        // annotation documentation support
        root + 'lib/local/annodoc.js',
        // project-specific collection data
        root + 'lib/local/collections.js',
        // project-specific configuration
        root + 'lib/local/config.js'
        );


        var webFontURLs = [
        root + 'static/fonts/PT_Sans-Caption-Web-Regular.ttf',
        root + 'static/fonts/Liberation_Sans-Regular.ttf'
        ];

        head.ready(function() {
            // mark current collection (filled in by Jekyll)
            Collections.listing['_current'] = '{{ page.collection }}';

        // performs all embedding and support functions
        Annodoc.activate(Config.bratCollData, Collections.listing);
        });


    </script>
</html>