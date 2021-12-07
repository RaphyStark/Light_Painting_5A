// SimpleTRx


// ATTENTION : il faut ajouter des conditions if pour que la carte soit l'un ou l'autre
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define CE_PIN   9
#define CSN_PIN 10


// for both
const byte slaveAddress[5] = {'R','x','A','A','A'};
RF24 radio(CE_PIN, CSN_PIN); // Create a Radio

// for receiver
char dataReceived[10]; // this must match dataToSend in the TX
bool newData = false;

// for transmitter
char dataToSend[10] = "Message 0";
char txNum = '0';
unsigned long currentMillis;
unsigned long prevMillis;
unsigned long txIntervalMillis = 1000; // send once per second


void setup() {

    Serial.begin(9600);
    Serial.println("Starting");
    radio.begin();
    radio.setDataRate( RF24_250KBPS );
    // for transmitter
    radio.setRetries(3,5); // delay, count
    radio.openWritingPipe(0xF0F0F0F0E1);
    // for receiver
    radio.openReadingPipe(1, thisSlaveAddress);
    radio.startListening();
    
}

void loop() 
{
    // for transmitter
    currentMillis = millis();
    if (currentMillis - prevMillis >= txIntervalMillis) 
    {
        send();
        prevMillis = millis();
    }
    // for receiver
    getData();
    showData();
}


// for transmitter
void send() {

    bool rslt;
    rslt = radio.write( &dataToSend, sizeof(dataToSend) );
        // Always use sizeof() as it gives the size as the number of bytes.
        // For example if dataToSend was an int sizeof() would correctly return 2

    Serial.print("Data Sent ");
    Serial.print(dataToSend);
    if (rslt) {
        Serial.println("  Acknowledge received");
        updateMessage();
    }
    else {
        Serial.println("  Tx failed");
    }
}

//================
// for transmitter
void updateMessage() {
        // so you can see that new data is being sent
    txNum += 1;
    if (txNum > '9') {
        txNum = '0';
    }
    dataToSend[8] = txNum;
}

// for receiver
void getData() 
{
    if ( radio.available() ) 
    {
        radio.read( &dataReceived, sizeof(dataReceived) );
        newData = true;
        
    }
    Serial.println(dataReceived);
}

// for receiver
void showData() 
{
    if (newData == true) 
    {
        Serial.print("Data received ");
        Serial.println(dataReceived);
        newData = false;
        delay(500);
    }
}

