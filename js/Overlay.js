
/**
 * Classe décrivant la fenêtre d'upload de documents.
 */
class Overlay{

    static accepted_types = ["CoNLL-U", "XML", "TXT"]
    static available_processors = ["stanza", "spacy"]
    static max_size = 1000.0;

    /**
     * Constructeur de la classe.
     * @param {String} id l'id à donner au widget
     * @param {jQuery} parent le parent dans lequel placer l'overlay
     */
    constructor(id, parent){

        this.div = $("<div id=\"" + id + "\" title=\"Ajouter des documents\">").appendTo(parent);
        var overlay_form = $("<form class=\"overlay_form\"></form>").appendTo(this.div);
        overlay_form.append("<input type=\"submit\" tabindex=\"-1\" style=\"position:absolute; top:-1000px\">");

        var left_section = $("<section class=\"overlay_section overlay_left\"></section>").appendTo(overlay_form);
        var right_section = $("<section class=\"overlay_section\"></section>").appendTo(overlay_form);

        var table = $("<table id=\"import_files_table\" class=\"display\"><thead><tr><th>Fichier</th><th>Taille (ko)</th><th>Type</th></tr></thead><tbody></tbody></table>").appendTo(left_section);
        this.filePicker = $("<input type=\"file\" name=\"filePicker\" multiple></input>").appendTo(left_section).button();


        var type_changer = $("<div id=\"type_changer\"></div>").appendTo(right_section);
        $("<legend><h2>Format de fichier</h2></legend>").appendTo(type_changer);

        this.selectType = $("<select name=\"selectType\" id=\"selectType\"></select>").appendTo(type_changer);

        this.changeTypeBtn = $("<button id=\"changeTypeBtn\" type=\"button\">Changer</button>").appendTo(type_changer).button();
        this.changeTypeBtn.on({"click": (function(){
            var dataind = this.table.rows({selected: true}).indexes();
            var type = this.selectType.val();

            dataind.toArray().forEach(el => this.table.cell(el, 2).data(type).draw());

            this.check();


            /*this.table.clear();
            this.table.rows.add(data);
            this.table.draw();*/
            
        }).bind(this)});

        this.processors = $("<div id=\"processors\"></div>").appendTo(right_section);
        $("<legend><h2>Processeurs</h2></legend>").appendTo(this.processors);

        $("<label for=\"tokenizer\">Tokeniseur</select>").appendTo(this.processors);
        this.tokenizer = $("<select id=\"tokenizer\"></select>").appendTo(this.processors);

        $("<label for=\"tagger\">Etiqueteur</select>").appendTo(this.processors);
        this.tagger = $("<select id=\"tagger\"></select>").appendTo(this.processors);

        $("<label for=\"lemmatizer\">Lemmatiseur</select>").appendTo(this.processors);
        this.lemmatizer = $("<select id=\"lemmatizer\"></select>").appendTo(this.processors);

        $("<label for=\"dependency_analyzer\">Analyseur syn.</select>").appendTo(this.processors);
        this.dependency_analyzer = $("<select id=\"dependency_analyzer\"></select>").appendTo(this.processors);


        Overlay.accepted_types.forEach(function(el){$("#selectType").append("<option value=\"" + el + "\">" + el + "</option>");});
        Overlay.available_processors.forEach(function(el){
            $("#tokenizer").append("<option value=\"" + el + "\">" + el + "</option>");
            $("#tagger").append("<option value=\"" + el + "\">" + el + "</option>");
            $("#lemmatizer").append("<option value=\"" + el + "\">" + el + "</option>");
            $("#dependency_analyzer").append("<option value=\"" + el + "\">" + el + "</option>");
        });

        //$("#selectType").selectmenu( "refresh" );

        this.alertFormat = $("<p class=\"ui-state-error\"><span class=\"ui-icon ui-icon-alert\"></span> Un ou plusieurs fichiers ne sont pas dans un format valide !</p>").appendTo(right_section);
        this.alertFormat.hide();

        this.alertSize = $("<p class=\"ui-state-error\"><span class=\"ui-icon ui-icon-alert\"></span> La taille totale des fichiers dépasse 1 Mo !</p>").appendTo(right_section);
        this.alertSize.hide();
        
        this.table = table.DataTable({
            select: 'multi+shift',
            lengthChange: false,
            paging: false,
            info: false,
            scrollResize: true,
            scrollY: 370,
            width: "100%",
            scrollCollapse: true,
        });

        this.dialog = this.div.dialog({
            autoOpen: false,
            height: 760,
            width: 1000,
            modal: true,
            resizable: false,
            draggable: false,
            buttons: {
                Ajouter: (function(){
                    this.addDocs();
                }).bind(this),
                Annuler: (function() {
                    this.hide();
                }).bind(this)
            },
            close: (function() {
                form[ 0 ].reset();
                this.hide();
                //allFields.removeClass( "ui-state-error" );
            }).bind(this)
        });


        this.selectType.selectmenu();
        this.tokenizer.selectmenu();
        this.tagger.selectmenu();
        this.lemmatizer.selectmenu();
        this.dependency_analyzer.selectmenu();

        this.processors.controlgroup({
            "direction": "vertical"
        });

        this.processors.controlgroup('disable');

        type_changer.controlgroup({
            "direction": "horizontal"
        });

        this.progressDialog = $("<div id=\"progressDialog\" title=\"Traitement\"></div>").dialog({
            autoOpen: false,
            resizable: false,
            draggable: false
        });

        var pBar = $("<div id=\"pBarUpload\"></div>").appendTo(this.progressDialog);

        pBar.progressbar({
            value: false
        });

        var form = this.dialog.find( "form" ).on( "submit", (function( event ) {
            event.preventDefault();
            this.addDocs();
        }).bind(this));

        this.allFields = $( [] ).add( this.filePicker ).add( this.table );

        this.filePicker.on("change", {overlay : this}, (function(event){
            this.fileList = event.target.files;

            /*if(typeof event.data.select.files === 'undefined'){
                event.data.select.files = [];
            }
            let names = event.data.select.files.map(a => a.name);*/

            event.data.overlay.table.clear();

            for(let i=0; i < this.fileList.length; i++){

                
                //if(!names.includes(fileList.item(i).name)){
                let type = this.fileList.item(i).type;
                let name = this.fileList.item(i).name;
                let size = this.fileList.item(i).size/1000;

                switch(type){

                    case "text/xml":
                        type = "XML";
                        break;
                    case "text/tab-separated-values":
                        type = "CoNLL-U";
                        break;
                    case "text/plain":
                        type = "TXT";
                        break;
                    default:
                        type = "";
                }

                if(type == ""){
                    switch(name.split('.').at(-1)){
                        case "conllu":
                            type = "CoNLL-U";
                            break;
                        case "xml":
                            type = "XML";
                            break;
                        case "tsv":
                            type = "CoNLL-U";
                            break;
                        default:
                            type = "";
                    }
                }

                event.data.overlay.table.row.add([name, size, type]);

            }

            this.check();

        }).bind(this));

        this.id = id;
    }

    /**
     * Méthode pour afficher la boîte de dialogue.
     */
    show(){
        this.dialog.dialog( "open" );
    }

    /**
     * Méthode pour cacher et réinitialiser la boîte de dialogue.
     */
    hide(){
        this.allFields.removeClass( "ui-state-error" );
        this.processors.controlgroup('disable');
        this.alertFormat.hide();
        this.alertSize.hide();
        this.table.clear().draw();
        this.dialog.dialog( "close" ); 
    }

    /**
     * Méthode envoyant les fichiers sélectionnés au serveur pour les traiter.
     * @returns bool
     */
    addDocs(){

        var data = new FormData();

        data.append("username", "bourdije");
        data.append("password", "password");
        
        for(let i=0; i < this.fileList.length; i++){
            data.append("file_" + i, this.fileList.item(i));
        }

        this.loading(true);

        $.ajax({
            url : "upload.php",
            method : "POST",
            dataType : "html",
            data : data,
            cache: false,
            contentType: false,
            processData: false,
            success : (function(result, status){
                this.loading(false);
                alert("Fichiers envoyés !");
                
            }).bind(this),
            error : (function(response, status, errorType){
                this.loading(false);
                $("<div>" + errorType + " : <p>" + response.responseText + "</p></div>").dialog();
            }).bind(this)
        });

        this.hide();
        return true;
    }

    /**
     * Méthode vérifiant l'intégrité du tableau des fichiers sélectionnés, et le mettant à jour.
     */
    check(){
        this.alertFormat.hide();
        this.alertSize.hide();

        let size = 0;
        let hasTxt = false;
        let error = false;

        for(let i=0; i < this.table.rows()[0].length; i++){

            size += this.table.cell(i, 1).data();

            if(!(Overlay.accepted_types.includes(this.table.cell(i, 2).data()))){
                //$(event.target).addClass( "ui-state-error" );
                $(this.table.row(i).node()).addClass("ui-state-error");
                this.alertFormat.show();
                error = true;
            }
            else{
                $(this.table.row(i).node()).removeClass("ui-state-error");
            }

            if(this.table.cell(i, 2).data() == "TXT"){
                hasTxt = true;
            }
        }

        if(size > Overlay.max_size){
            this.alertSize.show();
            error = true;
        }
        else{
            this.alertSize.hide();
        }

        if(error){
            $(".ui-dialog-buttonpane button:contains('Ajouter')").button('disable');
        }
        else{
            $(".ui-dialog-buttonpane button:contains('Ajouter')").button('enable');
        }

        if(!hasTxt){
            this.processors.controlgroup('disable');
        }
        else{
            this.processors.controlgroup('enable');
        }

        this.table.draw();
    }

    /**
     * Méthode permettant de contrôler l'affichage de la fenêtre de progression de l'upload.
     * @param {bool} toggle true: afficher false: cacher
     */
    loading(toggle){
        if(toggle){
            this.progressDialog.dialog('open');
        }
        else{
            this.progressDialog.dialog('close');
        }
        
    }
}