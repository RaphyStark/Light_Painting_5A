"""
A simple example of sending data from 1 nRF24L01 transceiver to another.
This example was written to be used on 2 devices acting as 'nodes'.
"""
import sys
import struct
from RF24 import RF24, RF24_PA_LOW



radio = RF24(22, 0)

uL = 200
uR = 250


if __name__ == "__main__":

    if not radio.begin():
        raise RuntimeError("radio hardware is not responding")

    address = [b"1Node", b"2Node"]
    radio_number = 1

    radio.setPALevel(RF24_PA_LOW)

    radio.openWritingPipe(address[radio_number])

    radio.openReadingPipe(1, address[not radio_number])

    radio.payloadSize = len(struct.pack("ii", uL, uR))

    
    buffer = struct.pack("ii", uL, uR)

    result = radio.write(buffer)
    if not result:
        print("Transmission failed")
    else:
        print("OK")

    radio.powerDown()
    sys.exit()
