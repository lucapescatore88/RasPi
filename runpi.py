import sys
sys.path.append("/home/pi/runpi/libraries")

#import RPi.GPIO as io
from board import Board
import subprocess as sb
from JobManager import JobManager
import json, os, sys

b = Board()
tmp = "/home/pi/runpi/server/tmp/"

def read_sensors(inpt,outpt) :

    file = open(tmp+"/potentiometer.json","w")
    file.write(str(b.pin_pot.read()))
    file.close()
    
    obj = {"motion" : "OFF", "sound" : "OFF"}
    if b.pin_motion.read() > 0.5 : obj["motion"] = "ON"
    if b.pin_sound.read() < 0.5 : obj["sound"] = "ON"
    #print b.pin_motion.read(), b.pin_sound.read()
    
    s = json.dumps(obj)
    file = open(tmp+"/sensors.json","w")
    file.write(s)
    file.close()

def set_motor(inpt,outpt) : 

    data = open(tmp+"/motor.json").read()
    obj  = json.loads(data)
    if obj["set"] == 'ACT' :
        print int(obj["state"])
        b.pin_motor.write(int(obj["state"]))
        obj["set"] = 'STILL'
        f = open(tmp+"/motor.json","w")
        f.write(json.dumps(obj));
        f.close()

def set_lcd(inpt,outpt) : 

    data = open(tmp+"/lcd.json").read()
    obj  = json.loads(data)
    if obj["set"] == 'ACT' :

        msg = ""
        if 'message0' in obj : msg = '{0:16}\n'.format(obj['message0'][:16])
        if 'message1' in obj : msg += '{0:16}'.format(obj['message1'][:16])
        
        b.lcd.clear() 
        b.lcd.message(msg)
        obj["set"] = 'STILL'
        f = open(tmp+"/lcd.json","w")
        f.write(json.dumps(obj));
        f.close()

def switch_tree(inpt,outpt) :

    data = open(tmp+"tree.json").read()
    if 'ON' in data : b.output("tree",True)
    else : b.output("tree",False)
      
def set_camera(inpt,outpt) :

    fname = "/home/pi/runpi/server/tmp/camera.json"
    data = open(fname).read()
    try: obj = json.loads(data)
    except ValueError, e: return

    out = sb.check_output("ps -h | grep start_camera.py",shell=True).split("\n")
    out = [ x for x in out if 'grep' not in x ]
    if obj["state"] == "ON":
        if len(out) < 2 : os.system("python /home/pi/runpi/start_camera.py &")
    elif len(out) > 1 :
        os.system("ps -h | grep start_camera.py | awk '{print $1}' | xargs kill -9")
 

jm = JobManager()
jm.add_process("sensors",read_sensors,interval=0.1)
jm.add_process("camera",set_camera,interval=0.5)
jm.add_process("lcd",set_lcd,interval=0.1)
jm.add_process("tree",switch_tree,interval=0.1)
jm.add_process("motor",set_motor,interval=0.1)
jm.run()







