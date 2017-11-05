
import datetime
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

loc = "/home/pi/runpi/server/tmp/"
d = {'hist':[0]*24, "entries" : 1 }
pickle.dump(d,open(loc+"stats.pkl","w"),protocol=pickle.HIGHEST_PROTOCOL)

def build_stats(inpt,output) :

    h = int(datetime.datetime.now().hour)
    fname = loc+"stats.pkl"
    with open(fname,'r') as f :
        stats = pickle.load(open(fname))
    
    if motion : 
        stats["hist"][h] = stats["hist"][h]*stats["entries"] + 1
        stats["entries"] += 1
        stats["hist"] = [ x / stats["entries"] for x in stats["hist"]]
    
    plt.xkcd()
    plt.figure()
    plt.plot(range(0,24),stats["hist"])
    plt.xlabel('Daily hour')
    plt.ylabel('Movement')
    plt.savefig(loc+'stats.png')    
   
    with open(fname,"w") as f : 
        stats = pickle.dump(stats,f,protocol=pickle.HIGHEST_PROTOCOL)


build_stats(None,None)


