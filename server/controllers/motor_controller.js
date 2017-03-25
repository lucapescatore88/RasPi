var file = require('../config').tmpfiles.motor
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

    app.get('/api/motor/set', function (req, res) {

        var query = url.parse(req.url, true).query;
        query.set = "ACT"
        fs.writeFile(file, JSON.stringify(query), function(err) {
    
            if(err) return console.log(err);
            res.send("Success");
        });
    });

    app.get('/api/motor/read', function (req, res) {

        fs.readFile(file, "utf-8", function(err, data) {
    
            if(err) return console.log(err);
            res.send(data);
        });
     });
};


 
