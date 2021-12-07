import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
GPIO.setmode(GPIO.BCM)
pipes = [[0xE8E8F0F0E1], [0xF0F0F0F0E1]]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
#radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_250KBPS)
#radio.setPALevel(NRF24.PA_MAX)
#radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()

message = list("GETSTRING")
while len(message) <= 32:
    message.append(0)
while(1):
    start = time.time()
    radio.write(message)
    print ("Sent the message: {}".format(message))
    radio.startListening()
    while not radio.available():
        time.sleep(1 / 100)
        if time.time() - start >2:
            print("Time out.")
            break
    uniMessage = []
    radio.read(uniMessage, radio.getDynamicPayloadSize())
    print("Received:{}".format(uniMessage))
    print("Translating receivedMessage into unicode characters")
    string = ""
    for n in range(len(uniMessage)):
        # Decode into standard unicode set
        string+= chr(n)
    print("Message is: {}".format(string))
    radio.stopListening()
    time.sleep(1)