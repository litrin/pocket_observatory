import RPi.GPIO as GPIO
import dht11
import time
import serial
import re 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Sensor:
    pin = 0
    def __init__(self, pin):
        self.pin = pin
    
    def read(self):
        return None
    
    def __iter__(self):
        while True:
            yield self.read()

class TempratureSensor(Sensor):

    def read(self):
        instance = dht11.DHT11(pin=self.pin)
            
        result = instance.read()
        if result.is_valid():
            return (result.temperature, result.humidity)
        else:
            time.sleep(1)
            return self.read()
    

class LightingSensor(Sensor):

    def read(self):

        GPIO.setup(self.pin, GPIO.IN)
        if GPIO.input(self.pin):
            return 0
        return 1


class SensorPlatform(Sensor):
    column = {             
              "illumination": int,
              "lighting": bool,
              "temprature": float,
              "humidity":float,
            }
    
    def __init__(self, port = "/dev/ttyS0", bps=9600, timeout=1):
        self.port = port
        self.bps = bps
        self.timeout = timeout
        
        GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.output(40, GPIO.LOW)

    def weakup(self):
        # send signal to Larduino pin D2 to weak up sensor platform    
        GPIO.output(40, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(40, GPIO.LOW)
    
    def decode(self, raw):
        raw = raw.split(",")
        cov = {}
        for i, key in enumerate(self.column.keys()):
            cov[key] = self.column[key](raw[i])
            
        return cov
    
    def read(self):
        self.weakup()

        ser = serial.Serial(self.port, self.bps, timeout=self.timeout)
        result = 0
        regex = r"^\d[\d|\.]"
        while True:
            try:
                c = ser.readline().decode()
            except:
                pass
            
            if re.match(regex, c):
                result = self.decode(c)
                break
        ser.close()

        
        return result
    

if __name__ == "__main__":
    #sensor = TempratureSensor(16)
    sensor = SensorPlatform()
    c = 0
    for i in sensor:
        c += 1
        print(c, str(i))
        time.sleep(5)



