from pyfirmata import Arduino, util
import RPi.GPIO as io
import sys
from LCD import Adafruit_CharLCD as LCD

#rs, en, d4, d5, d6, d7, cols, lines
lcd = LCD(4,17,27,22,6,19,16,2)
#lcd.message("Ciao bella!!    \nBlablabla       ")

usb = '0'
if len(sys.argv) > 1  and sys.argv[1]!="reset" :
    usb = sys.argv[1] 

class Board :

    def __init__(self) :

        io.setwarnings(False)

        self.io = io
        self.board = Arduino('/dev/ttyACM'+usb)
        self.it = util.Iterator(self.board)
        self.it.start()

        self.ch = {}
        self.ch["tree"] = 21
        self.ch["rgb_r"] = 23
        self.ch["rgb_b"] = 24
        self.ch["rgb_g"] = 25 
        
        self.lcd = lcd

        io.setmode(io.BCM)
        io.setup(self.ch["tree"], io.OUT, initial = False)
        io.setup(self.ch["rgb_r"], io.OUT, initial = False)
        io.setup(self.ch["rgb_b"], io.OUT, initial = False)
        io.setup(self.ch["rgb_g"], io.OUT, initial = False)
        
        self.pin_motor  = self.board.get_pin('d:10:s')
        self.pin_sound  = self.board.get_pin('a:0:i')
        self.pin_pot    = self.board.get_pin('a:5:i')
        self.pin_motion = self.board.get_pin('a:1:i')
        self.pin_light  = self.board.get_pin('a:4:i')

        #self.test_pin  = self.board.analog[4]
        #self.test_pin.enable_reporting()
        
        #while self.pin_motor.read() is None : pass
        while self.pin_pot.read() is None : pass
        while self.pin_sound.read() is None : pass
        while self.pin_light.read() is None : pass

        print "Started"
        self.pin_motor.write(80)

    def output(self,name,value) :

        io.output(self.ch[name],value)
    
    def read(self,name) :

        io.input(self.ch[name])



