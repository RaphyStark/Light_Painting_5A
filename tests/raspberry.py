import sys
import struct
from RF24 import RF24, RF24_PA_LOW



radio = RF24(22, 0)

uL = 200
uR = 250
success = False

if __name__ == "__main__":

    if not radio.begin():
        raise RuntimeError("radio hardware is not responding")

    address = [b"1Node", b"2Node"]
    
    radio_number = 1
    
    radio.setPALevel(RF24_PA_LOW)

    radio.openWritingPipe(address[radio_number])

    radio.openReadingPipe(1, address[not radio_number])

    radio.payloadSize = len(struct.pack("ii", uL, uR))

    radio.stopListening()
    
    while (success == False) :
        buffer = struct.pack("ii", uL, uR)
        result = radio.write(buffer)

        if result:
            print("OK")
            success = True
        else :
            print("failed")

    radio.powerDown()
    sys.exit()