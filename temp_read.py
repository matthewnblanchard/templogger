#!/usr/bin/python

import smbus

bus = smbus.SMBus(1)    # Open /dev/i2c-1

TEMP_ADDR = 0x48        # Temp. sensor address

temp = bus.read_byte(TEMP_ADDR)

print temp

