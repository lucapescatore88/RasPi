import multiprocessing as mp
from Queue import Queue
from datetime import datetime

class Proc :

    def __init__(self,proc,target,triggers,interval,sched,inpt,outpt,last) :

        self.proc     = proc
        self.target   = target
        self.triggers = triggers
        self.interval = interval
        self.sched    = sched
        self.inpt     = inpt
        self.outpt    = outpt
        self.last     = last

class JobManager :

    processes = {}
    inpts = {}
    outpts = {}
    
    def __init__(self,name = "MyManager",verbose=False):

        self.name = name 
        self.verb = verbose

    def add_process(self,name,func,triggers=[],interval=None,schedule=[]) :

        self.inpts[name] = Queue()
        self.outpts[name] = Queue()
        self.processes[name] = Proc(
            proc     = mp.Process(target=func, args=(self.inpts[name],self.outpts[name])),
            target   = func, 
            triggers = triggers,
            interval = interval,
            sched    = schedule,
            inpt     = self.inpts[name],
            outpt    = self.outpts[name],
            last     = datetime.now()
            )

    def run(self) :

        while True :

            self.check_triggers()
            self.check_interval()
            self.check_scheduled()            

    def check_triggers(self) :

        for name,proc in self.processes.iteritems() :
            for trig in proc.triggers :
                
                #run = True
                #if proc.interval is not None :
                #if proc.proc.is_alive() :
                    #now = datetime.now()
                    #if (now - proc.last).total_seconds() < proc.interval :
                #    run = False
                
                if not proc.proc.is_alive() :
                    if trig(proc.inpt) : self.start(name)

    def check_interval(self) :

        for name,proc in self.processes.iteritems() : 
            if proc.interval is None : continue
            now = datetime.now() 
            if (now - proc.last).total_seconds() > proc.interval : 
                self.start(name)
                proc.last = now

    def check_scheduled(self) :
        
        for name,proc in self.processes.iteritems() :
            if len(proc.sched) == 0 : return
            if (datetime.now() - proc.sched[0]).total_seconds() >= 0:
                proc.sched = proc.sched[1:]
                self.start(name)
                print "Interval"

    def start(self, name) :
        
        myproc = self.processes[name]
        if not myproc.proc.is_alive() :
            if self.verb : print "Starting ", name
            myproc.proc = mp.Process(target = myproc.target, args=(myproc.inpt,myproc.outpt))
            myproc.proc.start()













