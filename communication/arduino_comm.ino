#include "RF24.h"

RF24 radio(7, 8);
//RF24 radio(22, 23);

long payload[2];
uint8_t pipe;
long uL = 0;
long uR = 0;


void setup()
{
  Serial.begin(9600);
  while (!Serial) {}

  while (!radio.begin()) 
  {Serial.println(F("radio hardware is not responding!!"));}
  radio.setPayloadSize(8);
  radio.startListening();
}


void loop()
{
  if (radio.available(&pipe))
  {
    radio.read(&payload, 8);
    uL = payload[0];
    uR = payload[1];
    Serial.print("uL : ");
    Serial.println(uL);
    Serial.print("uR : ");
    Serial.println(uR);
  }
}
