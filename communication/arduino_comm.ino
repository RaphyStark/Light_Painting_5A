/*--------------------------------------------------------
   BORDURE.ino
   Boucle ouverte
  ------------------------------------------------------*/
/*        COMM*/
#include <SPI.h>
//#include "printf.h"
#include "RF24.h"
#include "math.h"


// instantiate an object for the nRF24L01 transceiver
RF24 radio(7, 8); // using pin 7 for the CE pin, and pin 8 for the CSN pin

//RF24 radio(22, 23);

// Let these addresses be used for the pair
uint8_t address[][6] = {"1Node", "2Node"};
// It is very helpful to think of an address as a path instead of as
// an identifying device destination

// to use different addresses on a pair of radios, we need a variable to
// uniquely identify which address this radio will use to transmit
bool radioNumber = 1; // 0 uses address[0] to transmit, 1 uses address[1] to transmit


long payload = 0;

uint8_t pipe;

bool test = false;

/*        END RADIO       */



void setup()
{
  /*        SERIAL          */
  // some boards need to wait to ensure access to serial over USB
  Serial.begin(115200);
  while (!Serial) {
    /* wait */
  }

  /*        RADIO           */
  // initialize the transceiver on the SPI bus
  while (!radio.begin()) {
    Serial.println(F("radio hardware is not responding!!"));
  }

  // Set the PA Level low to try preventing power supply related problems
  // because these examples are likely run with nodes in close proximity to
  // each other.
  radio.setPALevel(RF24_PA_LOW);  // RF24_PA_MAX is default.
  
  // save on transmission time by setting the radio to only transmit the
  // number of bytes we need to transmit a float
  // 1 octet  = 8 bits
  // 4 octets = 32 bits (1 float)
  // 2 octets = 16 bits

  //radio.setPayloadSize(sizeof(payload)); // float datatype occupies 32 bits
  radio.setPayloadSize(8);
  // set the TX address of the RX node into the TX pipe
  // forcé à 1 pour recevoir
  radio.openWritingPipe(address[1]);

  // set the RX address of the TX node into a RX pipe
  //radio.openReadingPipe(1, address[!radioNumber]); // using pipe 1
  radio.openReadingPipe(1, address[!1]); // using pipe 1

  radio.startListening(); // put radio in RX mode
  //Serial.println("setup end");
}


void loop()
{

 
  if (radio.available(&pipe))
  {
    uint8_t bytes = radio.getPayloadSize(); // get the size of the payload
    radio.read(&payload, bytes); // fetch payload from FIFO
    Serial.println(bytes);      // print the size of the payload
    Serial.println(payload);    // print the payload's value
    //Serial.println("radio available");
  }

  
  else
  {
    Serial.println("nothing around");
  }

  delay(1000);
  
  //Serial.println(sizeof(payload));
  //Serial.println(payload);
  
  /*
  if (test == false)
  {
    Serial.println("start loop");
    test = true;
  }
  */
}
