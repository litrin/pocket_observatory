import RPi.GPIO as GPIO
import dht11
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Sensor:
    pin = 0
    def __init__(self, pin):
        self.pin = pin
        
    def __iter__(self):
        yield None

class TempratureSensor(Sensor):

    def read(self):
        instance = dht11.DHT11(pin=self.pin)

        result = instance.read()
        if result.is_valid():
            return (result.temperature, result.humidity)
        else:
            time.sleep(1)
            return self.read()
    
    def __iter__(self):
        while True:
            yield self.read()

class LightingSensor(Sensor):

    def read(self):

        GPIO.setup(self.pin, GPIO.IN)
        if GPIO.input(self.pin):
            return 0
        return 1

    def __iter__(self):
        GPIO.setup(self.pin, GPIO.IN)
        #GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        while True:
            if GPIO.input(self.pin):
                yield 0
            else:
                yield 1
    

if __name__ == "__main__":
    #sensor = TempratureSensor(16)
    sensor = LightingSensor(18)
    
    for i in sensor:
        time.sleep(1)
        print(i)


