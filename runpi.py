import sys
sys.path.append("/home/pi/runpi/libraries")

#import RPi.GPIO as io
from board import Board
from JobManager import JobManager
import json

b = Board()
tmp = "/home/pi/runpi/server/tmp/"

def read_sensors(inpt,outpt) :
    s = json.dumps({"state":b.pin_pot.read()})
    file = open(tmp+"/potentiometer.json","w")
    file.write(s)
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
        b.lcd.message(obj["message"])
        obj["set"] = 'STILL'
        f = open(tmp+"/lcd.json","w")
        f.write(json.dumps(obj));
        f.close()



def switch_tree(inpt,outpt) :
    data = open(tmp+"tree.json").read()
    obj  = json.loads(data)
    
    if obj["state"] == 'ON' : b.output("tree",True)
    else : b.output("tree",False)
      


jm = JobManager()
jm.add_process("sensors",read_sensors,interval=0.1)
jm.add_process("lcd",set_lcd,interval=0.1)
jm.add_process("tree",switch_tree,interval=0.1)
jm.add_process("motor",set_motor,interval=0.1)
jm.run()







