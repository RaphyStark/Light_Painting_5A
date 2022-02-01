#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN       13
#define NUMPIXELS 7
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() 
{

    Serial.begin(9600);
    while (!Serial) {}

    pixels.begin();
    neopixel(0, 0, 0, 0);
    Serial.println("done");
    delay(1000);
} // setup


void loop() 
{
  neopixel(0, 255, 255, 255);
}


void neopixel(int ledNum, int R, int G, int B)
{
    pixels.clear();
    pixels.show();
    pixels.setPixelColor(ledNum, pixels.Color(R, G, B));
    pixels.show();
}
