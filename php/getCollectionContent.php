<?php

// Fortement inspiré de : https://codeanddeploy.com/blog/php/jquery-datatables-ajax-php-and-mysql-using-pdo-example

include ('connexion.php');

$searchQuery = " ";

if(isset($_POST['draw']) && isset($_POST['start']) && isset( $_POST['length']) && isset($_POST['order']) && isset($_POST['columns']) && isset($_POST['search'])){
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
            sents LIKE :sents OR
            tokens LIKE :tokens OR 
            lemmas LIKE :lemmas ) ";
        $searchArray = array( 
            'document_name'=>"%$searchValue%",
            'sents'=>"%$searchValue%",
            'tokens'=>"%$searchValue%",
            'lemmas'=>"%$searchValue%"
        );
    }

    // Total number of records with filtering
    $stmt = $pdo->prepare("SELECT COUNT(*) AS allcount FROM document WHERE 1 ".$searchQuery);
    $stmt->execute($searchArray);
    $records = $stmt->fetch();
    $totalRecordwithFilter = $records['allcount'];
}



// Total number of records without filtering
$stmt = $pdo->prepare("SELECT COUNT(*) AS allcount FROM document ");
$stmt->execute();
$records = $stmt->fetch();
$totalRecords = $records['allcount'];



// Fetch records

if(isset($columnName) && isset($columnSortOrder)){
    $stmt = $pdo->prepare("select document_name, count(distinct(sentence)) as sents, count(distinct(token_id)) as tokens, count(distinct(lemma_id)) as lemmas from collection\njoin collection_has_document on collection_has_document.collection_id = collection.collection_id\njoin document on document.document_id = collection_has_document.document_id\njoin sentence on sentence.text_id = document.document_id\njoin token on token.sentence = sentence.sentence_id\njoin lemma on lemma.lemma_id = token.lemma where 1 ".$searchQuery." group by document.document_id order by ".$columnName." ".$columnSortOrder." limit :limit,:offset");
    
    foreach ($searchArray as $key=>$search) {
        $stmt->bindValue(':'.$key, $search,PDO::PARAM_STR);
    }
    
    $stmt->bindValue(':limit', (int)$row, PDO::PARAM_INT);
    $stmt->bindValue(':offset', (int)$rowperpage, PDO::PARAM_INT);
}
else{
    $stmt = $pdo->prepare("select document_name, count(distinct(sentence)) as sents, count(distinct(token_id)) as tokens, count(distinct(lemma_id)) as lemmas from collection\njoin collection_has_document on collection_has_document.collection_id = collection.collection_id\njoin document on document.document_id = collection_has_document.document_id\njoin sentence on sentence.text_id = document.document_id\njoin token on token.sentence = sentence.sentence_id\njoin lemma on lemma.lemma_id = token.lemma where 1 ".$searchQuery." group by document.document_id order by document_name");
}

// Bind values

$stmt->execute();

$docRecords = $stmt->fetchAll();

$data = array();

foreach ($docRecords as $row) {
    $data[] = array(
        "document_name"=>$row['document_name'],
        "sents"=>$row['sents'],
        "tokens"=>$row['tokens'],
        "lemmas"=>$row['lemmas']
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