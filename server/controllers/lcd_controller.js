var file = require('../config').tmpfiles.lcd
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

app.get('/api/lcd/set', function (req, res) {

        var query = url.parse(req.url, true).query;
        query.set = "ACT";
        fs.writeFile(file, JSON.stringify(query), function(err) {
    
            if(err) return console.log(err);
            res.send("Success");
        });
    });
}

 
