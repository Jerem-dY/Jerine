<?php 

include ('connexion.php');
include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_GET["document"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}


function escape(string $input){
    if($input == '\n'){
        return '\\n';
    }
    else if($input == '\t'){
        return '\\t';
    }
    else if($input == '\r'){
        return '\\r';
    }
    else{
        return $input;
    }
}

$doc = $_GET["document"];
?>

<?php 
$sql = "SELECT COUNT(DISTINCT(sentence.sentence_id)) AS nb_sent FROM sentence
WHERE sentence.text_id = $doc;
";

if(!($response = $pdo->query($sql))){
    echo "<br/>Failed to fetch document's number of sentences. Aborting.<br/>";
    http_response_code(500);
    exit;
}

while($record = $response->fetch()){
    $sentence_total = $record["nb_sent"];
}

?>

<label for=<?php $sent = "sent_".$_GET["document"]; echo $sent;?>>Phrase (/<?php echo $sentence_total;?>)</label>
<input type="number" max=<?php echo $sentence_total;?> min="1" value="1" id=<?php $sent = "sent_".$_GET["document"]; echo $sent;?> name=<?php $sent = "sent_".$_GET["document"]; echo $sent;?> ></input>
<script>
    $(<?php echo $sent;?>).on("change", function(){
        $.ajax({
            url: "php/get_deprel_view.php",
            method : "GET",
            dataType : "html",
            data : "document="+<?php echo $_GET["document"]; ?>+"&sentence="+$(<?php $sent = "sent_".$_GET["document"]; echo $sent;?>).val(),
            success : (function(result, status){

                $(<?php echo "conllu_".$_GET["document"];?>).text(result);
                Annodoc.activate(Config.bratCollData, Collections.listing);

            }).bind(this),
            error : (function(response, status, errorType){
                $("<div>" + errorType + " : <p>" + response.responseText + "</p></div>").dialog();
            }).bind(this)
        });
    });
</script>
<div class="conllu-parse" tabs="yes" style="width: 1000px;" id=<?php echo "conllu_".$_GET["document"];?>>
<?php 

if(isset($_GET) && isset($_GET["sentence"])){

    $sent_nb = $_GET["sentence"];
    $query = "SELECT token_sent_ind as ID, tok_form.form_chars as FORM, lem_form.form_chars as LEMMA, lemma.pos as UPOS, token.head as HEAD, token.deprel as DEPREL, token.offset as OFFSET, token.spaceafter as SPACEAFTER FROM token
    INNER JOIN lemma ON token.lemma = lemma.lemma_id
    INNER JOIN form AS tok_form ON token.token_form = tok_form.form_id
    INNER JOIN form AS lem_form ON lemma.lemma_form = lem_form.form_id
    INNER JOIN sentence ON sentence.sentence_id = token.sentence
    INNER JOIN document ON sentence.text_id = document.document_id

    WHERE document.document_id = $doc AND sentence.sentence_doc_ind = $sent_nb;
    ";

    if(!($response = $pdo->query($query))){
        echo "<br/>Failed to fetch document's content. Aborting.<br/>";
        http_response_code(500);
        exit;
    }

    $lines = 0;
    while($record = $response->fetch()){

        if($record["ID"] == 1){
            $lines++;
            echo "\n# sent_id = $lines\n";
        }

        $id = $record["ID"];
        $form = escape($record["FORM"]);
        $lemma = escape($record["LEMMA"]);
        $upos = $record["UPOS"];
        $head = $record["HEAD"];
        $deprel = $record["DEPREL"];
        $misc = ($record["SPACEAFTER"] == 0) ? "SpaceAfter=No" : "_";

        if($upos == "SPACE"){
            $form = " ";
            $lemma = " ";
        }

        echo "$id\t$form\t$lemma\t$upos\t_\t_\t$head\t$deprel\t_\t$misc\n";
    }
}


?>
</div>


<script type="text/javascript">
    Annodoc.activate(Config.bratCollData, Collections.listing);
</script>