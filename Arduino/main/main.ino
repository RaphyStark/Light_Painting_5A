/*--------------------------------------------------------
    Principal changement : j'ai retiré output du constructeur du PID
 ------------------------------------------------------*/


// objects for motors encoders
#include <Encoder.h>
  Encoder leftEnc(19, 18);
  Encoder rightEnc(20, 21);

/*
byte inducPin;
byte pwmPin;
byte dirPin;
*/


// le temps entre deux appels du PID 
double time_in_loop = 2;
double lastTime;
double newTime;

// la condition d'arrêt du contrôle moteur
// à changer par un nombre de ticks / position à atteindre donnée par capteurs externes
unsigned long duration = 10000;

// à utiliser quand on aura une position atteinte en fin de while
bool stop_control;


// objects for the PID
#include <PID_Lib.h>
int16_t leftInput;
int16_t rightInput;
int16_t leftLastInput;
int16_t rightLastInput;

byte leftDirPin = 2;
byte rightDirPin = 8;

byte leftPwmPin = 3;
byte rightPwmPin = 9;

byte pwm = 127;

//float output = 0;
int16_t leftSetpoint = 50;
int16_t rightSetpoint = 50;
double Kp = 10, Ki = 0, Kd = 0;

PID leftPID(&leftInput/*, &output$*/, &leftSetpoint, Kp, Ki, Kd);
PID rightPID(&rightInput/*, &output*/, &rightSetpoint, Kp, Ki, Kd);

// On met en place les neopixels
#include <Adafruit_NeoPixel.h> // se trouve dans la bibliothèque de librairies d'Arduino IDE
#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN       8
#define NUMPIXELS 7
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
clock_prescale_set(clock_div_1);
#endif
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
// Left and right motors with corresponding pins
#include <motor.h>
Motor leftMotor(leftPwmPin, leftDirPin);
Motor rightMotor(rightPwmPin, rightDirPin);


// ASSERVISSEMENT
//double now = 0;
//double go = 0;


int k = 0;
int DEB = 1;

void setup() 
{
  Serial.begin(115200);
  pixels.begin();
  neopixel(0, 0, 0, 0);
  //wait(2000);
}

void loop() 
{
  if (k == 0)
  { 
    Serial.println("Hello");
    control_func();
    //stopMotors();
    k = 1;
  }
}




void neopixel(int ledNum, int R, int G, int B)
{
  pixels.clear();
  pixels.show();
  pixels.setPixelColor(ledNum, pixels.Color(R, G, B));
  pixels.show();
}


/*
void wait(double waitTime)
{
  now = millis();
  go = millis() - now;
  while (go < waitTime)
  {
    go = millis() - now;
  }
}
*/

/*
void stopMotors()
{
  DEB = 1;
  //move(0, 0, 500);
  rightMotor.stop();
  leftMotor.stop();
  DEB = 1;
}
*/

//
