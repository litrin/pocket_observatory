// #include <PMU.h>
#include <DHT.h>

#define TIME_OUT 5000
#define INTERVAL_SECONDS 60

const uint8_t lightSensorDigital = D7;
const uint8_t lightSensorAnalog = A0;
const int lightSensorRange[2] = {200, 3000};

const uint8_t dthPin = A3;
DHT dht(dthPin, DHT11);

volatile bool counter = true;

void setup()
{
  Serial.begin(9600);
  
//  attachInterrupt(0, send_data, HIGH);  
//  pinMode(D2, INPUT);
//  digitalWrite(D2, LOW);
  
  pinMode(lightSensorDigital, INPUT);
  pinMode(lightSensorAnalog, INPUT);

  dht.begin();
  Serial.println("LT sensor platform is ready!");

}

int read_lighting(bool digi=false)
{
  if (digi)
  {
    return digitalRead(lightSensorDigital);
  }else{
    return map(analogRead(lightSensorAnalog), lightSensorRange[0], lightSensorRange[1], 100, 1);
  }
}

int read_temprature(int types)
{
//  Serial.println("DHT11 sensor");

  float v;
  if (types == 0)
  {
     v = dht.readHumidity();
  }else{
     v = dht.readTemperature();
  }

  if (isnan(v)) {
    return 0;
  }
  return v;
}

void loop()
{
//  send_data();
  
//  Serial.flush();
//  PMU.sleep(PM_POFFS0);  

  send_data();
  delay(INTERVAL_SECONDS * 1000);
  
}


void send_data()
{ 
//  detachInterrupt(0);

  String msg = String(read_lighting());
  msg += ",";
  msg += String(read_temprature(1));
  msg += ",";
  msg += String(read_temprature(0));

  Serial.println(msg);
  digitalWrite(D2, LOW);
  delay(TIME_OUT);

//  attachInterrupt(0, send_data, HIGH); 


}
