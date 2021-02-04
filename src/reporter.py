import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
    
GPIO.setmode(GPIO.BOARD)

class Signal:
    gpio = [8,10,12]
    blink_interval = 0.1
    R = 0
    Y = 1
    G = 2
    
    curr = 0
    
    def __init__(self, r=8, g=12, y=10, interval=0.2):
        self.gpio = [r, y, g]

        self.interval = interval
        for i in self.gpio:
            GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
    
    def blink(self, a, loop=3):
        i = 0
        while i < loop:
            i += 1

            GPIO.output(self.gpio[a], GPIO.HIGH)
            sleep(self.blink_interval)
            GPIO.output(self.gpio[a], GPIO.LOW) 
            sleep(self.blink_interval) 
            
    def open(self, a):
        self.blink(a)
        GPIO.output(self.gpio[a], GPIO.HIGH)
        self.curr = a
        
    def close(self, a):
        self.blink(a)
        GPIO.output(self.gpio[a], GPIO.LOW)
    
    def switch(self, a):
        self.close(self.curr)
        self.open(a)
        
        

if __name__ == "__main__":
    signal = Signal()
    while True:
        signal.open(signal.R)
        signal.open(signal.Y)
        signal.open(signal.G)
        
        sleep(10)
        
        signal.close(signal.R)
        signal.close(signal.Y)
        signal.close(signal.G)
        
        sleep(10)
        
    RPi.GPIO.clean()
