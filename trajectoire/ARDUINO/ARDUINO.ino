// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        6 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 7 // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels






/*
  * See documentation at https://nRF24.github.io/RF24
  * See License information at root directory of this library
  * Author: Brendan Doherty (2bndy5)
  */
  
 #include <SPI.h>
 #include "printf.h"
 #include "RF24.h"
 #include "math.h"

  
 // instantiate an object for the nRF24L01 transceiver
 RF24 radio(7, 8); // using pin 7 for the CE pin, and pin 8 for the CSN pin
  
 // Let these addresses be used for the pair
 uint8_t address[][6] = {"1Node", "2Node"};
 // It is very helpful to think of an address as a path instead of as
 // an identifying device destination
  
 // to use different addresses on a pair of radios, we need a variable to
 // uniquely identify which address this radio will use to transmit
 bool radioNumber = 1; // 0 uses address[0] to transmit, 1 uses address[1] to transmit
  
 // Used to control whether this node is sending or receiving
 bool role = false;  // true = TX role, false = RX role
  
 // For this example, we'll be using a payload containing
 // a single float number that will be incremented
 // on every successful transmission
 float payload = 0.0;
 bool payloadnb=0;
  
 void setup() {
   Serial.begin(115200);
   while (!Serial) {
     // some boards need to wait to ensure access to serial over USB
   }



  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear();

  pixels.setPixelColor(0, pixels.Color(0, 0, 150));
   pixels.show();
   // initialize the transceiver on the SPI bus
   while (!radio.begin()) {
     Serial.println(F("radio hardware is not responding!!"));
    
   }
  
   // print example's introductory prompt
   Serial.println(F("RF24/examples/GettingStarted"));
  
   // To set the radioNumber via the Serial monitor on startup
   //Serial.println(F("Which radio is this? Enter '0' or '1'. Defaults to '0'"));
   //while (!Serial.available()) {
     // wait for user input
   //}
   //char input = Serial.parseInt();
   radioNumber = 0;//input == 1;
   Serial.print(F("radioNumber = "));
   Serial.println((int)radioNumber);
  
   // role variable is hardcoded to RX behavior, inform the user of this
   //Serial.println(F("*** PRESS 'T' to begin transmitting to the other node"));
  
   // Set the PA Level low to try preventing power supply related problems
   // because these examples are likely run with nodes in close proximity to
   // each other.
   radio.setPALevel(RF24_PA_LOW);  // RF24_PA_MAX is default.
  
   // save on transmission time by setting the radio to only transmit the
   // number of bytes we need to transmit a float
   radio.setPayloadSize(sizeof(payload)); // float datatype occupies 4 bytes
  
   // set the TX address of the RX node into the TX pipe
   radio.openWritingPipe(address[radioNumber]);     // always uses pipe 0
  
   // set the RX address of the TX node into a RX pipe
   radio.openReadingPipe(1, address[!radioNumber]); // using pipe 1
  
   // additional setup specific to the node's role
   if (role) {
     radio.stopListening();  // put radio in TX mode
   } else {
     radio.startListening(); // put radio in RX mode
   }
  
   // For debugging info
   // printf_begin();             // needed only once for printing details
   // radio.printDetails();       // (smaller) function that prints raw register values
   // radio.printPrettyDetails(); // (larger) function that prints human readable data
  
 } // setup
  
 void loop() {
  
   if (role) {
     // This device is a TX node
  
     unsigned long start_timer = micros();                    // start the timer
     bool report = radio.write(&payload, sizeof(float));      // transmit & save the report
     unsigned long end_timer = micros();                      // end the timer
  
     if (report) {
       Serial.print(F("Transmission successful! "));          // payload was delivered
       Serial.print(F("Time to transmit = "));
       Serial.print(end_timer - start_timer);                 // print the timer result
       Serial.print(F(" us. Sent: "));
       Serial.println(payload);                               // print payload sent
       payload += 0.01;                                       // increment float payload
     } else {
       Serial.println(F("Transmission failed or timed out")); // payload was not delivered
     }
  
     // to make this example readable in the serial monitor
     delay(1000);  // slow transmissions down by 1 second
  
   } else {
     // This device is a RX node
     uint8_t pipe;
     
     float V,Omega;
     if (radio.available(&pipe)) {             // is there a payload? get the pipe number that recieved it
       uint8_t bytes = radio.getPayloadSize(); // get the size of the payload
       radio.read(&payload, bytes);            // fetch payload from FIFO
       Serial.print(F("\nReceived "));
       Serial.print(bytes);                    // print the size of the payload
       Serial.print(F(" bytes on pipe "));
       Serial.print(pipe);                     // print the pipe number
       Serial.print(F(": "));
       Serial.print(payload);                // print the payload's value
       Serial.print("\n"); 
       if (payloadnb==0)
       {
        V=payload;
        Serial.print("V: "); 
        Serial.print(V);
        
       }
       if (payloadnb==1) {
        Omega=payload;
        Serial.print("Omega: "); 
        Serial.print(Omega); 
       }
       if (payloadnb==1){
        payloadnb=0;
       }else payloadnb=1;
       
        
       
       
     }
   } // role
  
   if (Serial.available()) {
     // change the role via the serial monitor
  
     char c = toupper(Serial.read());
     if (c == 'T' && !role) {
       // Become the TX node
  
       role = true;
       Serial.println(F("*** CHANGING TO TRANSMIT ROLE -- PRESS 'R' TO SWITCH BACK"));
       radio.stopListening();
  
     } else if (c == 'R' && role) {
       // Become the RX node
  
       role = false;
       Serial.println(F("*** CHANGING TO RECEIVE ROLE -- PRESS 'T' TO SWITCH BACK"));
       radio.startListening();
     }
   }
  
 } // loop