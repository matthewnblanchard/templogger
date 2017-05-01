#!/usr/bin/python

import smbus
import sqlite3
import time
from datetime import date, datetime

# Set up I2C communication with the temperature sensor
bus = smbus.SMBus(1)    # Open /dev/i2c-1
TEMP_ADDR = 0x48        # Temp. sensor address

# SQL database setup
db = sqlite3.connect("temp.db")   # Connect to the database
cursor = db.cursor()              # Obtain cursor for data entry

# Create the temp/date table
db.execute("CREATE TABLE IF NOT EXISTS temps([timestamp] timestamp, temperature integer)")


def add_temp():

        temp = bus.read_byte(TEMP_ADDR) # Read current temperature
        
        cursor.execute("INSERT INTO temps (timestamp, temperature) \
        VALUES (?, ?)", (datetime.now(), temp))
        db.commit()

while True:
        add_temp()
        time.sleep(60)

