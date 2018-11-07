// from data.js
var tableData = data;

// YOUR CODE HERE!
var tbody = d3.select("tbody")

// fill table with data
data.forEach((tableRow) => {
    var row = tbody.append("tr");

    Object.values(tableRow).forEach((value) => {
        var cell = row.append("td");
        cell.text(value);
    })
})


// prevent from refreshing
d3.event.preventDefault();

//filter date search