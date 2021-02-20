
#include <PMU.h>
#include <DHT.h>

#define TIME_OUT 5000
#define INTERVAL_SECONDS 60
#define SLEEP true 
#define INT 0

const uint8_t lightSensorDigital = D11;
const uint8_t lightSensorAnalog = A0;
const int lightSensorRange[2] = {50, 2000};

const uint8_t dthPin = A3;

DHT dht(dthPin, DHT11);

void setup()
{
  Serial.begin(9600);  

  pinMode(D2, INPUT_PULLUP);
  
  pinMode(lightSensorDigital, INPUT);
  pinMode(lightSensorAnalog, INPUT);

  dht.begin();
  Serial.println("LT sensor platform is ready!");
  
  if (SLEEP)
  {
    attachInterrupt(INT, weakup, HIGH);  // set interrupt
  }

}

int read_lighting(bool digi=false)
{
  if (digi)
  {
    return digitalRead(lightSensorDigital) == 1 ? 0 : 1;
  }else{
    return map(analogRead(lightSensorAnalog), lightSensorRange[0], lightSensorRange[1], 100, 1);
  }
}

float read_temprature(int types)
{

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
//  Serial.println("INT 0: " + String(digitalRead(D2)));
  String msg = String() ;
  
  msg = String(read_lighting());
  msg += ",";
  msg += String(read_lighting(true));
  msg += ",";
  
  msg += String(read_temprature(1), 1);
  msg += ",";
  msg += String(read_temprature(0), 1);

  Serial.println(msg);
  delay(TIME_OUT);

  
  if (SLEEP)
  {
//  Serial.println("go to sleeping");
    Serial.flush();
    attachInterrupt(INT, weakup, HIGH); 
    PMU.sleep(PM_POFFS0);  // sleep forever till  INT 0
  }
  else{
    delay(INTERVAL_SECONDS * 1000);
  }
  
}


void weakup()
{ 
  detachInterrupt(INT);
}
