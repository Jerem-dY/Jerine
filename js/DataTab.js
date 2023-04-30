



/**
 * Classe représentant l'onglet de gestion des documents de l'interface graphique.
 */
class DataTab{

    /**
     * Constructeur de la classe.
     * @param {String} id l'identifiant à donner au widget
     * @param {jQuery} parent le parent du widget
     */
    constructor(id, manager){

        // Création des éléments HTML
        this.div = $("<div id=\"" + id + "\" title=\"Ajouter des documents\" class=\"central_area\">").appendTo(manager.div);
        this.div.controlgroup();
        this.documentsTable = $("<table id=\"collection_content_table\" class=\"refresh refreshtable cell-border hover stripe display\">\
        <thead>\
            <tr>\
                <th>Document</th>\
                <th>Phrases</th>\
                <th>Tokens</th>\
                <th>Lemmes</th>\
                <th>Formes</th>\
                <th>Rapport types/tokens</th>\
                <th>Caractères</th>\
            </tr>\
        </thead>\
    </table>").appendTo(this.div);
    this.addFilesBtn = $("<button id=\"addFiles\">Ajouter des documents</button>").appendTo(this.div);
    this.removeFilesBtn = $("<button id=\"removeFiles\">Supprimer des documents</button>").appendTo(this.div);

    this.overlay = new Overlay("add_documents", $("body"));

    // Quand on clique sur le bouton d'ajout de fichiers
    this.addFilesBtn.button().on( "click", (function() {
        this.overlay.show();
    }).bind(this));

    this.addFilesBtn.button("option", "icon", "ui-icon-plusthick");

    // Quand on clique sur le bouton de suppression de fichiers
    this.removeFilesBtn.button().on( "click", (function() {

        let collection_id = $("#collectiontree").jstree("get_selected", true)[0].original.collection_id;
        let document_ids = [];
        var data = $("#collection_content_table").DataTable().rows( { selected: true } ).data();

        for(let i = 0; i < data.length ; i++){
            document_ids.push(data[i]['id'])
        }

        var to_remove = new FormData();
        to_remove.append("document_ids", JSON.stringify(document_ids));
        to_remove.append("collection_id", collection_id);


        $.ajax({
            url : "./php/remove_documents.php",
            method : "POST",
            dataType : "html",
            data: to_remove,
            cache: false,
            contentType: false,
            processData: false,
            success : function(result, status){

                $(".refresh").trigger("refresh_tables");
                
            },
            error : function(response, status, errorType){
                alert("Une erreur est survenue en tentant de supprimer les documents : " + errorType + " - " + response.responseText);
            }
        });

    }).bind(this));

    this.removeFilesBtn.button("option", "icon", "ui-icon-closethick");


    // Mise en place de la requête ajax pour récupérer le contenu de la collection courante
    var data = new FormData();
    data.append("collection_id", $("#collectiontree").jstree("get_selected", true)[0].original.collection_id);

    this.documentsTable.DataTable({
        'processing': true,
        'serverSide': true,
        "scrollY": "240px",
        select: true,
        'serverMethod': 'post',
        dataSrc: 'aaData',
        'ajax': {
            'url':'php/get_collection_content.php?collection_id='+$("#collectiontree").jstree("get_selected", true)[0].original.collection_id
        },
        'columns': [	
            { data: 'document' },
            { data: 'sentences' },
            { data: 'tokens' },
            { data: 'lemmas' },
            { data: 'forms' },
            { data: 'typetokenr' },
            { data: 'chars' },
            { data: 'id',
              visible: false}
        ]
    });

    // Quand on double-clique sur une document dans le tableau, on ouvre un onglet pour visualiser son contenu
    $('#collection_content_table > tbody').on( 'dblclick', 'tr',function () { 
        var data = $("#collection_content_table").DataTable().row(this).data();

        let name = data["document"].replace(".", "_")

        if($("#"+name).length == 0){
            manager.addTab(name, data["id"]);
        }

    }); 


    }
}