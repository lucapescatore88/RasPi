var file = require('../config').tmpfiles.camera
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

    app.get('/api/camera/set', function (req, res) {

        var query = url.parse(request.url, true).query;
        fs.writeFile(file, JSON.stringify(query), function(err) {
    
            if(err) return console.log(err);
            res.send("Success");
        });
    });

}


 
