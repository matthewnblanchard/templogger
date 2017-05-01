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

## Lighttpd setup
Lighttpd was set up and configured to run a python script for the webpage. By default,
the Raspberry Pi 3 uses Apache to run a web server. This was stopped using the following command:
        update-rc.d apache2 disable
Following this, the lighttpd package was installed:
        sudo apt-get install lighttpd
Lighttpd is automatically set to start at boot when installed

A configuration file was made for CGI, for use with the python script:
        /etc/lighttpd/conf.d/cgi.conf
        /----------------------------/
        server.modules += ("mod\_cgi")
        
        cgi.assign =            ( ".pl"  => "/usr/bin/perl",
                                  ".php" => "/usr/bin/php-cgi",
                                  ".py"  => "/usr/bin/python" )
        
        index-files.names +=    ( "index.pl",  "default.pl",
                                  "index.php", "default.php",
                                  "index.py",  "default.py" )

The following line was added to /etc/lighttpd/lighttpd.conf
        include "conf.d/cgi.conf"

## Webpage Setup
The webpage is generated using a python script, templogger.py. The script operates by querying
the SQLite3 database populated by read\_temp.py for all rows with timestamps less than a day old, 
converting the timestamps into floating point numbers, and plotting them versus the temperatures. The plot
is then saved to an image which is displayed on the page via html.
