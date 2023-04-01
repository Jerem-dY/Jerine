<?php

// Fortement inspiré de : https://codeanddeploy.com/blog/php/jquery-datatables-ajax-php-and-mysql-using-pdo-example

include ('connexion.php');
include("start_session.php");


$searchQuery = " ";


$draw = $_POST['draw'];
$row = $_POST['start'];
$rowperpage = $_POST['length']; // Rows display per page
$columnIndex = $_POST['order'][0]['column']; // Column index
$columnName = $_POST['columns'][$columnIndex]['data']; // Column name
$columnSortOrder = $_POST['order'][0]['dir']; // asc or desc
$searchValue = $_POST['search']['value']; // Search value

$searchArray = array();

if($searchValue != ''){
    $searchQuery = " AND (document_name LIKE :document_name ) ";
    $searchArray = array( 
        'document_name'=>"%$searchValue%"
    );
}
 
// Total number of records with filtering
$stmt = $pdo->prepare("SELECT COUNT(*) AS allcount 
FROM document 
JOIN collection_has_document ON collection_has_document.document_id = document.document_id 
WHERE collection_has_document.collection_id=".$_GET["collection_id"]." ".$searchQuery);
$stmt->execute($searchArray);
$records = $stmt->fetch();
$totalRecordwithFilter = $records['allcount'];



// Total number of records without filtering
$stmt = $pdo->prepare("SELECT COUNT(*) AS allcount 
FROM document 
JOIN collection_has_document ON collection_has_document.document_id = document.document_id 
WHERE collection_has_document.collection_id=".$_GET["collection_id"]." ");
$stmt->execute();
$records = $stmt->fetch();
$totalRecords = $records['allcount'];



// Fetch records


$stmt = $pdo->prepare("select document.document_id as did, document_name as document, count(distinct(sentence)) as sentences, count(distinct(token_id)) as tokens, count(distinct(lemma_id)) as lemmas, count(distinct(token.token_form)) as forms, sum(form.form_len) as chars, count(distinct(token.token_form))/count(distinct(token_id)) as typetokenr from collection
join collection_has_document on collection_has_document.collection_id=collection.collection_id
join document on collection_has_document.document_id = document.document_id
join sentence on sentence.text_id = document.document_id
join token on token.sentence = sentence.sentence_id
join lemma on token.lemma = lemma.lemma_id
join form on form.form_id = token.token_form
where collection.collection_id=".$_GET["collection_id"]." ".$searchQuery." group by document.document_id order by document_name");

$stmt = $pdo->prepare("select document.document_id as did, document_name as document, count(distinct(sentence)) as sentences, count(distinct(token_id)) as tokens, count(distinct(lemma_id)) as lemmas, count(distinct(token.token_form)) as forms, sum(form.form_len) as chars, count(distinct(token.token_form))/count(distinct(token_id)) as typetokenr from collection
join collection_has_document on collection_has_document.collection_id=collection.collection_id
join document on collection_has_document.document_id = document.document_id
join sentence on sentence.text_id = document.document_id
join token on token.sentence = sentence.sentence_id
join lemma on token.lemma = lemma.lemma_id
join form on form.form_id = token.token_form
where collection.collection_id=".$_GET["collection_id"]." ".$searchQuery." group by document.document_id order by ".$columnName." ".$columnSortOrder." limit :limit,:offset");

foreach ($searchArray as $key=>$search) {
    $stmt->bindValue(':'.$key, $search,PDO::PARAM_STR);
}

$stmt->bindValue(':limit', (int)$row, PDO::PARAM_INT);
$stmt->bindValue(':offset', (int)$rowperpage, PDO::PARAM_INT);

// Bind values

$stmt->execute();

$docRecords = $stmt->fetchAll();

$data = array();

foreach ($docRecords as $row) {
    $data[] = array(
        "document"=>$row['document'],
        "sentences"=>$row['sentences'],
        "tokens"=>$row['tokens'],
        "lemmas"=>$row['lemmas'],
        "forms"=>$row['forms'],
        "typetokenr"=>$row['typetokenr'],
        "chars"=>$row['chars'],
        "id"=>$row['did'],
    );
}

if(isset($_POST['draw'])){
    $response = array(
        "draw" => intval($draw),
        "iTotalRecords" => $totalRecords,
        "iTotalDisplayRecords" => $totalRecordwithFilter,
        "aaData" => $data
    );
}
else{
    $response = array("aaData" => $data);
}



header("Content-Type: application/json; charset=utf-8");
echo json_encode($response);

?>