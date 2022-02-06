#include "RF24.h"
#include "motor.h"
#include <Encoder.h>
Encoder leftEnc(19, 18);
Encoder rightEnc(21, 20);
// On met en place les neopixels
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


// Left and right motors with corresponding pins
#include <motor.h>
Motor leftMotor(leftMotorPwmPin, leftMotorDirPin);
Motor rightMotor(rightMotorPwmPin, rightMotorDirPin);



// PID variables
double leftError = 0;
double leftSetpoint = 0;
double leftInput = 0;
double leftOutput = 0;
double rightError = 0;
double rightSetpoint = 0;
double rightInput = 0;
double rightOutput = 0;
double leftPrevOutput = 0;
double rightPrevOutput = 0;
double leftKp = 0.07;
double rightKp = 0.07;
double totalTicksL = 0;
double totalTicksR = 0;
double totalTemps = 0;


// machine state
enum State_e {CHECK_RADIO, COMPUTE};
State_e state;


//RF24 radio(7, 8);
RF24 radio(22, 23);


uint8_t address[][6] = {"1Node", "2Node"};
bool radioNumber = 0;
bool role = false;

long payload[2];
uint8_t pipe;
long wG = 0;
long wD = 0;


void setup()
{
  state = CHECK_RADIO;
  
  // init serial
  Serial.begin(9600);
  while (!Serial) {}

  //init pixels
  pixels.begin();
  neopixel(0,100,100,100);
  // init radio
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
  switch (state)
  {
    case CHECK_RADIO :
      if (radio.available(&pipe))
      {
      uint8_t bytes = radio.getPayloadSize(); 
      radio.read(&payload, bytes);
      wD = payload[0];
      wG = payload[1];
      Serial.println("new setpoints received !");
      Serial.print("new wG : ");
      Serial.println(wG);
      Serial.print("new wD : ");
      Serial.println(wD);
      state = COMPUTE;
      //delay(3000);
      }
/*
      else
      {
      Serial.print("wG : ");
      Serial.println(wG);
      Serial.print("wD : ");
      Serial.println(wD);
      }
*/
    break;
    
    
    case COMPUTE :
      compute(wD, wG);
      state = CHECK_RADIO;
    break;
  }
}



void compute(double rightSetpoint, double leftSetpoint)
{
  if (leftSetpoint == 0 && rightSetpoint == 0)
  {
    stopMotors();
  }

  else
  {
    totalTicksL = leftEnc.read();
    totalTicksR = rightEnc.read();
  
    leftInput = leftEnc.read() - totalTicksL;
    rightInput = rightEnc.read() - totalTicksR;
    totalTicksL = leftEnc.read();
    totalTicksR = rightEnc.read();
  
    leftError = leftSetpoint - leftInput;
    rightError = rightSetpoint - rightInput;
  
    leftOutput = leftPrevOutput + leftKp * leftError;
    rightOutput = rightPrevOutput + rightKp * rightError;
  
    if (leftOutput > 250)   leftOutput = 250;
    if (rightOutput > 250)  rightOutput = 250;
    if (leftOutput < -250)     leftOutput = -250;
    if (rightOutput < -250)    rightOutput = -250;
  
    leftPrevOutput  = leftOutput;
    rightPrevOutput = rightOutput;
  
    leftMotor.setU(leftOutput);
    rightMotor.setU(rightOutput);
  
    // printInfos();
    // i = i + 1;
  
    // laisser le setU faire effet avant de recalculer l'output
    double lastTime = millis();
    double newTime = millis() - lastTime;
    while (newTime < 150)
    {
      newTime = millis() - lastTime;
    }
  }
}


void stopMotors()
{
  Serial.println();
  Serial.println();
  //Serial.println("Stop motors");
  leftMotor.setU(-30);
  rightMotor.setU(-30);
  delay(100);
  leftMotor.setU(-15);
  rightMotor.setU(-15);
  delay(100);
  leftMotor.setU(-10);
  rightMotor.setU(-10);
  delay(100);
  leftMotor.setU(-5);
  rightMotor.setU(-5);
  delay(100);
  rightMotor.stop();
  leftMotor.stop();
}

void neopixel(int ledNum, int R, int G, int B)
{
  pixels.clear();
  pixels.show();
  pixels.setPixelColor(ledNum, pixels.Color(R, G, B));
  pixels.show();
}
