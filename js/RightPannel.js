

/**
 * CLasse représentant le pannel droit de l'interface graphique (à définir).
 */
class RightPannel{

    /**
     * Constructeur de la classe.
     * @param {String} id l'identifiant à donner au widget
     * @param {jQuery} parent le parent du widget
     */
    constructor(id, parent){

        this.div = $("<div id=\"" + id + "\" class=\"rightpannel ui-corner-all ui-widget ui-widget-content\">").appendTo(parent);

    }
}