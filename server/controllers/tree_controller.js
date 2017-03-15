var file = require('../config').tmpfiles.tree
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

app.get('/api/tree/set', function (req, res) {

    var query = url.parse(request.url, true).query;
    fs.writeFile(file, JSON.stringify(query), function(err) {
    
        if(err) return console.log(err);
        res.send("Success");
    });
}

app.get('/api/tree/read', function (req, res) {

    fs.readFile(file, function(err,data) {
    
        if(err) return console.log(err);
        res.json(data);
    });
}


 
