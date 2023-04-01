


/**
 * Classe représentant le gestionnaire d'onglets de l'interface graphique.
 */
class TabManager{

    /**
     * Constructeur de la classe.
     * @param {String} id l'identifiant à donner au widget
     * @param {jQuery} parent le parent du widget
     */
    constructor(id, parent){

        this.div = $("<div id=\"" + id + "\">").appendTo(parent);
        this.headers = $("<ul id=\"tab_headers\"><li id=\""+ id +"\"><a href=\"#datatab\">Documents</a></li>").appendTo(this.div);
        
        this.datatab = new DataTab("datatab", this);

        var postData = {};

        this.div.tabs({
            select: function(event, ui) {
                postData = {
                    document: parseInt($(ui.tab).data('id'))
                };
            },
            ajaxOptions: {
                type: 'POST',
                data: postData,
                error: function(xhr, status, index, anchor) {
                    $(anchor.hash).html("Couldn't load this tab.");
                }
            }
        });

        var manager = this;

        this.div.on( "click", "span.ui-icon-close", (function() {
            var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
            $( "#" + panelId ).remove();
            manager.div.tabs( "refresh" );
        }));

    }

    addTab(text, id){
        var newTab = new ViewTab(text, id, this);
        this.div.tabs( "refresh" );
        this.div.tabs( "option", "active", -1 );
    }

    



}