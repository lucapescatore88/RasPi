var file = require('../config').tmpfiles.motion
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

    app.get('/api/motion/set', function (req, res) {

        var query = url.parse(request.url, true).query;
        fs.writeFile(file, JSON.stringify(query), function(err) {
    
            if(err) return console.log(err);
            res.send("Success");
        });
    });

    app.get('/api/motion/read', function (req, res) {

        fs.readFile(file, "utf-8", function(err,data) {
    
            if(err) return console.log(err);
            res.send(data);
        });
    });

    app.get('/api/motion/stats', function (req, res) {

        res.sendFile("/home/pi/runpi/server/images/stats.png");
    });


}
 
