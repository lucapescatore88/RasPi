var express = require('express')
var app = express()

var motionCtrl = require('controllers/motion_controller')
var lcdCtrl = require('controllers/lcd_controller')
var cameraCtrl = require('controllers/camera_controller')

app.get('/', function (req, res) {
  res.send(req.url)
})

motionCtrl(app)
lcdCtrl(app)
cameraCtrl(app)

app.listen(3000)



