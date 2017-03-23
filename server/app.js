var express = require('express');
var app = express();

var motionCtrl = require('./controllers/motion_controller');
var lcdCtrl = require('./controllers/lcd_controller');
var cameraCtrl = require('./controllers/camera_controller');
var potCtrl = require('./controllers/potentiometer_controller');
var treeCtrl = require('./controllers/tree_controller');

app.use('/',express.static(__dirname+'/public'));
app.use('/', function (req, res, next) {
  console.log(req.url);
  next();
});

motionCtrl(app);
lcdCtrl(app);
cameraCtrl(app);
potCtrl(app);
treeCtrl(app);

app.listen(3000,'192.168.0.66');



