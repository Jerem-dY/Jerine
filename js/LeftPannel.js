

/**
 * Classe représentant le pannel gauche de l'interface graphique, soit la partie "navigation".
 */
class LeftPannel{

    /**
     * Constructeur de la classe.
     * @param {String} id l'identifiant à donner au widget
     * @param {jQuery} parent le parent du widget
     */
    constructor(id, parent){

        this.div = $("<div id=\"" + id + "\" class=\"leftpannel ui-corner-all ui-widget ui-widget-content\">").appendTo(parent).resizable({
            containment: "#"+parent[0].id,
            handles: 'e',
            minWidth: 300
        });

        this.tree = $("<div id=\"collectiontree\" class=\"refresh refreshtree\">").appendTo(this.div);

        this.addColBtn = $("<button id=\"addColBtn\">+ collection</button>").appendTo(this.div).button().on("click", (function(){this.addColDialog.dialog( "open" );}).bind(this));
        this.deleteColBtn = $("<button id=\"deleteColBtn\">- collection</button>").appendTo(this.div).button().on("click", (function(){
            
            var data = new FormData();

            data.append("collection_id", this.tree.jstree("get_selected", true)[0].original.collection_id);

            $.ajax({
                url : "./php/remove_collection.php",
                method : "POST",
                dataType : "html",
                data : data,
                cache: false,
                timeout: 0,
                contentType: false,
                processData: false,
                success : (function(result, status){
                    window.location.href = window.location.href;
                    
                }).bind(this),
                error : (function(response, status, errorType){
                    $("<div>" + errorType + " : <p>" + response.responseText + "</p></div>").dialog();
                }).bind(this)
            });
        }).bind(this));

        this.addColDialog = $("<div id=\"addColDialog\"></div>").appendTo(this.div);

        this.tree.jstree({
            'core': {
                "themes" : { "stripes" : true },
                'data': {
                    'url': function(node) {
                        return 'php/get_collections.php';
                    },
                    'data': function(node) {
                        return {
                            'parent': node.id
                        };
                    }
                },
                "multiple": false
            }
        });

        this.addColDialog.dialog({
            autoOpen: false,
			hide: 'fold',
			show: 'blind',
            height: 200,
            width: 300,
            modal: true,
            resizable: false,
            draggable: true,
            buttons: {
                Ajouter: (function(){

                    var data = new FormData();

                    data.append("collection_name", this.newColName.val());

                    $.ajax({
                        url : "./php/add_collection.php",
                        method : "POST",
                        dataType : "html",
                        data : data,
                        cache: false,
                        timeout: 0,
                        contentType: false,
                        processData: false,
                        success : (function(result, status){
                            window.location.href = window.location.href;
                            
                        }).bind(this),
                        error : (function(response, status, errorType){
                            $("<div>" + errorType + " : <p>" + response.responseText + "</p></div>").dialog();
                        }).bind(this)
                    });

                    this.addColDialog.dialog( "close" );

                }).bind(this),
                Annuler: (function() {
                    this.addColDialog.dialog( "close" );
                }).bind(this)
            },
            close: (function() {
                this.newColName.val("");
            }).bind(this)
        });

        /*var form = $("<form>").appendTo(this.addColDialog);
        form.append("<input type=\"submit\" tabindex=\"-1\" style=\"position:absolute; top:-1000px\">");*/

        this.newColName = $("<input type=\"text\" name=\"newColName\">").appendTo(this.addColDialog);

        this.tree.on("changed.jstree", (function(){

            if(this.tree.jstree("get_selected", true)[0].id == "mes_documents"){
                this.deleteColBtn.button('disable');
            }
            else{
                this.deleteColBtn.button('enable');
            }

            $(".refresh").trigger("refresh_tables");
        }).bind(this));

    }
}