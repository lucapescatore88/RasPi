import sys
sys.path.append("/home/pi/runpi/libraries")

#import RPi.GPIO as io
from board import Board
import subprocess as sb
from JobManager import JobManager
import json, os, sys

b = Board()
tmp = "/home/pi/runpi/server/tmp/"
img = "/home/pi/runpi/server/images/"

import datetime
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if len(sys.argv) > 1 and sys.argv[1]=="reset" : 
    d = {'hist':[0]*24, "entries" : 1 }
    pickle.dump(d,open(tmp+"stats.pkl","w"),protocol=pickle.HIGHEST_PROTOCOL)

def build_stats(inpt,output) :

    h = int(datetime.datetime.now().hour)
    fname = tmp+"stats.pkl"
    with open(fname) as f :
        stats = pickle.load(open(fname)) 
    if b.pin_motion.read() > 0.5 : 
        stats["hist"][h] = stats["hist"][h]*stats["entries"] + 1
        stats["entries"] += 1 
        
    stats["hist"] = [ x / stats["entries"] for x in stats["hist"]]
    
    plt.xkcd()
    plt.figure(figsize=(4, 3), dpi=100)
    plt.plot(range(0,24),stats["hist"])
    plt.xlabel('Daily hour')
    plt.ylabel('Movement')
    plt.savefig(img+'stats.png')    
   
    with open(fname,"w") as f : 
        pickle.dump(stats,f,protocol=pickle.HIGHEST_PROTOCOL)

def read_sensors(inpt,outpt) :

    file = open(tmp+"/potentiometer.json","w")
    file.write(str(b.pin_pot.read()))
    file.close()
    
    obj = {"motion" : "NO", "sound" : "NO", "light" : "NO"}
    if b.pin_motion.read() > 0.5 : obj["motion"] = "YES"
    if b.pin_sound.read() < 0.5 : obj["sound"] = "YES"
    if b.pin_light.read() < 0.3 : obj["light"] = "YES"
    #print b.pin_motion.read(), b.pin_sound.read()
    #print b.pin_light.read()

    s = json.dumps(obj)
    file = open(tmp+"/sensors.json","w")
    file.write(s)
    file.close()

def set_rgb(inpt,outpt) :

    with open(tmp+"/rgb.json") as f :
        data = f.read()
        try: obj = json.loads(data)
        except ValueError, e: return

    #print obj
    if obj["blue"] == 'true' : b.output("rgb_b",True)
    else : b.output("rgb_b",False)
    if obj["red"] == 'true' : b.output("rgb_r",True)
    else : b.output("rgb_r",False)
    if obj["green"] == 'true': b.output("rgb_g",True)
    else : b.output("rgb_g",False)

def set_motor(inpt,outpt) : 

    data = open(tmp+"/motor.json").read()
    obj  = json.loads(data)
    if obj["set"] == 'ACT' :
        b.pin_motor.write(int(obj["pos"]))
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
        msg.replace("_"," ")
       
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
jm.add_process("rgb",set_rgb,interval=0.1)
jm.add_process("stats",build_stats,interval=5)
jm.add_process("sensors",read_sensors,interval=0.1)
jm.add_process("camera",set_camera,interval=0.5)
jm.add_process("lcd",set_lcd,interval=0.1)
jm.add_process("tree",switch_tree,interval=0.1)
jm.add_process("motor",set_motor,interval=0.1)
jm.run()







