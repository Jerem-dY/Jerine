<?php

// Fortement inspiré de : https://codeanddeploy.com/blog/php/jquery-datatables-ajax-php-and-mysql-using-pdo-example

include ('connexion.php');

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
    $searchQuery = " AND (document_name LIKE :document_name OR 
        count(distinct(sentence)) LIKE :sentences OR
        count(distinct(token_id)) LIKE :tokens OR 
        count(distinct(lemma_id)) LIKE :lemmas OR
        count(distinct(token.token_form)) LIKE :forms OR
        count(distinct(token.token_form))/count(distinct(token_id)) LIKE :typtokenr OR
        sum(form.form_len) LIKE :chars ) ";
    $searchArray = array( 
        'document_name'=>"%$searchValue%",
        'sents'=>"%$searchValue%",
        'tokens'=>"%$searchValue%",
        'lemmas'=>"%$searchValue%",
        'forms'=>"%$searchValue%",
        'typetokenr'=>"%$searchValue%",
        'chars'=>"%$searchValue%"
    );
}

// Total number of records with filtering
$stmt = $pdo->prepare("SELECT COUNT(*) AS allcount FROM document WHERE 1 ".$searchQuery);
$stmt->execute($searchArray);
$records = $stmt->fetch();
$totalRecordwithFilter = $records['allcount'];



// Total number of records without filtering
$stmt = $pdo->prepare("SELECT COUNT(*) AS allcount FROM document ");
$stmt->execute();
$records = $stmt->fetch();
$totalRecords = $records['allcount'];



// Fetch records


$stmt = $pdo->prepare("select document_name as document, count(distinct(sentence)) as sentences, count(distinct(token_id)) as tokens, count(distinct(lemma_id)) as lemmas, count(distinct(token.token_form)) as forms, sum(form.form_len) as chars, count(distinct(token.token_form))/count(distinct(token_id)) as typetokenr from collection
join collection_has_document on collection_has_document.collection_id = collection.collection_id
join document on document.document_id = collection_has_document.document_id
join sentence on sentence.text_id = document.document_id
join token on token.sentence = sentence.sentence_id
join lemma on lemma.lemma_id = token.lemma
join form on form.form_id = token.token_form
where 1 ".$searchQuery." group by document.document_id order by document_name");

$stmt = $pdo->prepare("select document_name as document, count(distinct(sentence)) as sentences, count(distinct(token_id)) as tokens, count(distinct(lemma_id)) as lemmas, count(distinct(token.token_form)) as forms, sum(form.form_len) as chars, count(distinct(token.token_form))/count(distinct(token_id)) as typetokenr from collection
join collection_has_document on collection_has_document.collection_id = collection.collection_id
join document on document.document_id = collection_has_document.document_id
join sentence on sentence.text_id = document.document_id
join token on token.sentence = sentence.sentence_id
join lemma on lemma.lemma_id = token.lemma
join form on form.form_id = token.token_form
where 1 ".$searchQuery." group by document.document_id order by ".$columnName." ".$columnSortOrder." limit :limit,:offset");

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
        "chars"=>$row['chars']
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