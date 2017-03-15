import sys
sys.path.append("/home/pi/libraries")

from LCD import Adafruit_CharLCD as LCD

#rs, en, d4, d5, d6, d7, cols, lines
lcd = LCD(4,17,27,22,6,19,16,2)
lcd.message("Ciao bella!!    \nBlablabla       ")

