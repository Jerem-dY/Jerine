


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
        this.headers = $("<ul id=\"tab_headers\"><li><a href=\"#datatab\">Documents</a></li>").appendTo(this.div);
        
        this.datatab = new DataTab("datatab", this.div);

        this.div.tabs();

    }

    



}