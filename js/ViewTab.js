


class ViewTab{

    constructor(id, doc_id, tabmanager){

        this.header = $("<li><a href=\"php/get_deprel_view.php?document="+ doc_id +"\" class=\"viewtab\">"+ id +"</a><span class='ui-icon ui-icon-close' role='presentation' data-id=\""+ doc_id +"\"></span></li>").appendTo(tabmanager.headers);
        //this.content = $("<div id=\"" + id + "\" title=\""+ id +"\" class=\"central_area\">").appendTo(tabmanager.div);

    }
}