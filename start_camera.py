from picamera import PiCamera
from time import sleep
import json

camera = PiCamera()
camera.resolution = (1800, 1000)
camera.start_preview()

while True :

    fname = "/home/pi/runpi/server/tmp/camera.json"
    data = open(fname).read()
    try: obj = json.loads(data)
    except ValueError, e: continue

    if obj["capture"] == "ACT":
        obj["capture"] = "STILL"
        camera.resolution = (640, 360)
        camera.capture("/home/pi/runpi/server/images/capture.jpg")
        camera.resolution = (1800, 1000)
        f = open(fname,"w")
        f.write(json.dumps(obj))
        f.close()
    
    if obj["eff"] in camera.IMAGE_EFFECTS: 
        camera.image_effect = obj["eff"]
    else : camera.image_effect = "none"
    
    if 'note' in obj :
        camera.annotate_text = obj['note']

#camera.stop_preview()


