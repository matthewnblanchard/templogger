# Description
This webpage displays temperature data polled from a TC74AO temperature sensor connected to the I2C
bus on Raspberry Pi 3. Temperatures are polled in 1 minute intervals and plotted against time.

# Documentation
Following is a complete breakdown of the scripts/utilities used to set up the webpage.

## Hardware
The TC74AO temperature sensor communicates via I2C, and was connected to the I2C bus of the Raspberry
Pi 3. Four connections, to pins GND, 3.3V, I2C1 SDA, and I2C1 SCL were made. Operation was verified
using i2ctools. The sensor uses address 0x48, and read requests to it by default return the 
temperature. Temperature is read back in units of celsius.

## SQLite3 Database/Sensor Querying
The SQLite3 database and sensor querying are handled by a python script, temp\_read.py. 
Temperatures are stored in timestamp, temperature pairs in a table within the SQL database.
I2C communication is reliazed through the SMBus python module. The table is updated with current
information every 60 seconds
