
function flattenObj(obj, parent = '', res = {}){
    for(let key in obj){
        let propName = parent ? parent + '.' + key : key;
        if(typeof obj[key] == 'object'){
            flattenObj(obj[key], propName, res);
        } else {
            res[propName] = obj[key];
        }
    }
    return res;
}


let populateRow = (row, data) => {
  for (let prop in data)
    {
        if(typeof data[prop] === 'object' && data[prop] !== null)
        {
          populateRow(row, data[prop]);
        }
        else{
          let cell = row.insertCell(-1);
          cell.innerHTML = data[prop];
        }
    }
}

let getColumn = (row, data) => {
  for (let prop in data)
    {
        if(typeof data[prop] === 'object' && data[prop] !== null)
        {
          getColumn(row, data[prop]);
        }
        else{
          let cell = row.insertCell(-1);
          cell.innerHTML = prop;
        }
    }
}

let tableFromJson = (data) => {

    //let leaves = flattenObj(data);
    // Extract value from table header. 
    // ('Book ID', 'Book Name', 'Category' and 'Price')

    const table = document.createElement("table");
    let headers = false;

    for (let key in data) {
        
      let tr = table.insertRow(-1); 

        if(!headers)
      {
        getColumn(tr, data[key]);
        headers = true;
        continue;
      }
    
      populateRow(tr, data[key]);
    }

    return table;
  }

