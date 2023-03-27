



/**
 * Classe représentant l'onglet de gestion des documents de l'interface graphique.
 */
class DataTab{

    /**
     * Constructeur de la classe.
     * @param {String} id l'identifiant à donner au widget
     * @param {jQuery} parent le parent du widget
     */
    constructor(id, parent){

        this.div = $("<div id=\"" + id + "\" title=\"Ajouter des documents\" class=\"central_area\">").appendTo(parent);
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

    this.overlay = new Overlay("add_documents", $("body"));

    this.addFilesBtn.button().on( "click", (function() {
        this.overlay.show();
    }).bind(this));

    this.addFilesBtn.button("option", "icon", "ui-icon-document");

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
            { data: 'chars' }
        ]
    });


    }
}