
function structureJson(obj)
{
    obj.text = {};

    for (var k in obj)
    {
        if (typeof obj[k] == "object" && obj[k] !== null)
            structureJson(obj[k]);
        else{
            if (!obj.hasOwnProperty(k))
            {
                continue;  
            }
            if(k == "value"){
                delete obj[k];
            }
            if(k == parent){
                continue;
            }
            if (k != "children")
            {
                obj.text[k] = obj[k];
                delete obj[k];
            }
                // do something...
        }
    }
}



function create_chart(data, jq_container){

    //let beg = jsonview.create(xml2json(xml_data, ""));
    /*var x2js = new X2JS();
    let beg = x2js.xml_str2json(xml_data);*/

    //beg = structureJson(beg);

    chart_config = {    chart: {
        container: jq_container,
        connectors: {
            type: "straight",
            stackIndent: 15
        },
        levelSeparation: 300,
        siblingSeparation: 20,
        subTeeSeparation: 70,
        rootOrientation: "WEST",
        hideRootNode: "true"
    }, nodeStructure: data};

    return new Treant(chart_config, function() { alert( 'Tree Loaded' ) }, $ );
}



