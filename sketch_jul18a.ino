#include <DHT11.h>
#define pin 2
DHT11 dht11(pin);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial){
    
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  int err;
  float temperature, humidity;
  String msg;
  if(!(err=dht11.read(humidity,temperature))){
    msg = String(temperature) + "," + String(humidity);
    Serial.print(msg);
    delay(5000);
  }else{
    Serial.println("Error : " + err);
    delay(500);
  }
}
