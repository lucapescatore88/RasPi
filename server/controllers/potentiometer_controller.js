var file = require('../config').tmpfiles.potentiometer
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

    app.get('/api/potentiometer/read', function (req, res) {

        fs.readFile(file, "utf-8", function(err,data) {
    
            if(err) return console.log(err);
            res.send(data);
        });
     });
}


 
