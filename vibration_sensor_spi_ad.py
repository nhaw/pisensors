#!/usr/bin/python

import spidev
import time

spi = spidev.SpiDev()
spi.open(0,1)

spi0 = spidev.SpiDev()
spi0.open(0,0)

while True:
    #resp = spi.xfer2([0x00])
    #print resp
    data = spi.readbytes(2)
    val = ((data[0] & 0x1f) << 7) | (data[1] >> 1)
    print val, [bin(x) for x in data]

    data = spi0.readbytes(2)
    val = ((data[0] & 0x1f) << 7) | (data[1] >> 1)
    print 's0', val, [bin(x) for x in data]

    time.sleep(0.5)
