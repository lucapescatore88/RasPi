var file = require('../config').tmpfiles.tree
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

    app.get('/api/tree/set', function (req, res) {

        var query = url.parse(req.url, true).query;
        fs.writeFile(file, query.state, function(err) {
    
            if(err) return console.log(err);
            res.send("Success");
        });
    });

    app.get('/api/tree/read', function (req, res) {

        fs.readFile(file, "utf-8", function(err, data) {
    
            if(err) return console.log(err);
            res.send(data);
        });
     });
};


 
