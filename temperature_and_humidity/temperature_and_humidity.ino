#include "DHT.h"             // DHT sensors library
#define dhtPin 7             // This is data pin

#define dhtType DHT11        // This is DHT 11 sensor

DHT dht(dhtPin, dhtType);    // Initialising the DHT library

float humValue;           // value of humidity
float temperatureValueC;  // value of temperature in degrees Celcius

void setup() {
  Serial.begin(9600);        // Initialising the serial monitor
  dht.begin();               // start reading the value from DHT sensor
//  Serial.println("");
//  Serial.print("Humidity , ");
//  Serial.println("Temperature");
  
}

void loop() {

  humValue = dht.readHumidity();               // value of humidity
  temperatureValueC = dht.readTemperature();   // value of temperature in degrees Celcius
  
  // reading values from DHT sensor successfully or not
  if (isnan(humValue) || isnan(temperatureValueC)) {
    Serial.println("failed to reading from DHT sensor!");
  
    return;
}
  Serial.print(humValue);     // get value of humidity
  Serial.print(" , ");          // create space after the value of humidity
  Serial.println(temperatureValueC);  // get value of temperature in degrees Celcius
  delay(1000);  // print value after interval of time
}
