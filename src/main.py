from sensor import TempratureSensor, LightingSensor
from reporter import Signal
import RPi.GPIO as GPIO
import time
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'observatory')
client.create_database('observatory')

def save_db(values):
    global client
    points = [
        {
            "measurement": "observatory",
            "tags": {
            "region": "SH, myhome"
            }   ,

            "fields": values
        }
    ]
    return client.write_points(points, database='observatory')  

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def main(interval):
    temp = TempratureSensor(16)
    lighting = LightingSensor(18)
    signal = Signal(r=8, g=10,y=12)
    
    
    for h, t in temp:
        c = lighting.read()
        
        s = 2
        if t > 25 or t < 18:
            s -= 1
            
        if h > 70 or h < 40:
            s -= 1
        
        if s < 2:
            s += c

        signal.switch(s)
        print(h, t, c)
        save_db({"temprature": h, "humidity":t, "lighting":c, "comfort": s})
        
        time.sleep(interval)

if __name__ == "__main__":
    interval = 60
    # time.sleep(interval)

    main(interval)
