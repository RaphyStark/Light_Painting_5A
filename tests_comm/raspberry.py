"""
A simple example of sending data from 1 nRF24L01 transceiver to another.
This example was written to be used on 2 devices acting as 'nodes'.
"""
import sys
import time
import struct
from RF24 import RF24, RF24_PA_LOW

radio = RF24(22, 0)


uL = 200
uR = 250



success = False

if __name__ == "__main__":

    # initialize the nRF24L01 on the spi bus
    if not radio.begin():
        raise RuntimeError("radio hardware is not responding")

    # For this example, we will use different addresses
    # An address need to be a buffer protocol object (bytearray)
    address = [b"1Node", b"2Node"]
    # It is very helpful to think of an address as a path instead of as
    # an identifying device destination

    # to use different addresses on a pair of radios, we need a variable to
    # uniquely identify which address this radio will use to transmit
    # 0 uses address[0] to transmit, 1 uses address[1] to transmit
    radio_number = 0 # uses default value from `parser`

    # set the Power Amplifier level to -12 dBm since this test example is
    # usually run with nRF24L01 transceivers in close proximity of each other
    radio.setPALevel(RF24_PA_LOW)  # RF24_PA_MAX is default

    # set the TX address of the RX node into the TX pipe
    radio.openWritingPipe(address[radio_number])
    
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
        time.sleep(1)
