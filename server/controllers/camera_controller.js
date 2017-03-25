var file = require('../config').tmpfiles.camera
var fs = require('fs')
var url = require('url');

module.exports = function(app) {

    app.get('/api/camera/set', function (req, res) {

        var query = url.parse(req.url, true).query;
        query.capture = 'STILL';
        fs.writeFile(file, JSON.stringify(query), function(err) {
    
            if(err) { console.log(err); return; }
            res.send("Success");
        });
    });

    app.get('/api/camera/capture', function (req, res) {

        fs.readFile(file,function(err,data) {
            
            if(err) { console.log(err); return; }
            obj = JSON.parse(data);
            obj.capture = 'ACT';

            fs.writeFile(file, JSON.stringify(obj), function(err2) {
            
                if(err2) { console.log(err2); return; }
                setTimeout( function() {
                    res.sendFile("/home/pi/runpi/server/images/capture.jpg");
                });
            });
        });
    });

    app.get('/api/camera/getstats', function (req, res) {

            res.sendFile("/home/pi/runpi/server/images/stats.png");
    });

}


 
