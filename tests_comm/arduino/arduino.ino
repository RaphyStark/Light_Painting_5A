#include <SPI.h>
#include "printf.h"
#include "RF24.h"

RF24 radio(7, 8);
//RF24 radio(22, 23);


uint8_t address[][6] = {"1Node", "2Node"};
bool radioNumber = 1;
bool role = false;

long payload[2];
uint8_t pipe;
long uL = 0;
long uR = 0;


void setup()
{
  Serial.begin(9600);
  while (!Serial) {}

  // initialize the transceiver on the SPI bus
  if (!radio.begin()) {
    Serial.println(F("radio hardware is not responding!!"));
    while (1) {}} // hold in infinite loop
  radio.setPALevel(RF24_PA_LOW);
  radio.setPayloadSize(sizeof(payload));
  radio.openWritingPipe(address[radioNumber]);
  radio.openReadingPipe(1, address[!radioNumber]);
  radio.startListening();
}


void loop()
{
  if (radio.available(&pipe))
  {
    uint8_t bytes = radio.getPayloadSize(); 
    radio.read(&payload, bytes);
    uL = payload[0];
    uR = payload[1];
    Serial.print("uL : ");
    Serial.println(uL);
    Serial.print("uR : ");
    Serial.println(uR);
  }
  else
  {
    Serial.println("nothing");
  }
}
