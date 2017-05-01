#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import matplotlib
import matplotlib.dates as dates
import sqlite3
from datetime import datetime 

# Select non-GUI backend for matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# Connect to SQLite3 database
db = sqlite3.connect('temp.db')
cursor = db.cursor()

# Extract last 24 hours worth of rows
dat_time = []
dat_temp = []
for row in cursor.execute('''SELECT * FROM temps WHERE ((julianday('now') - julianday(timestamp)) <= 1)'''):
        dat_time.append(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
        dat_temp.append(row[1])

# Set plot font
plt.rcParams["font.family"] = "monospace"

# Create plot
fig = plt.figure()
ax = fig.add_subplot(111)

# Title plot
title = plt.title('Temperature Logs')
plt.setp(title, color = 'w')

# Configure plot axes
ax.set_ylim([0, 35])
ax.set_xlim([dates.date2num(datetime.now()) - 1, dates.date2num(datetime.now())])
ax.set_ylabel('Temperature (Degrees Celsius)')
ax.set_xlabel('Time/Date')
ax.xaxis.label.set_color('w')
ax.yaxis.label.set_color('w')
ax.set_axis_bgcolor('k')
ax.tick_params(color = 'w', labelcolor = 'w', which = 'both')
ax.grid(which = 'major', color = 'w', linestyle = '-', linewidth = 0.5)
ax.grid(which = 'minor', color = 'w', linestyle = '--', linewidth = 0.25)
ax.spines['bottom'].set_color('w')
ax.spines['top'].set_color('w')
ax.spines['left'].set_color('w')
ax.spines['right'].set_color('w')

hrloc = dates.HourLocator(byhour = range(1, 24))
dyloc = dates.DayLocator()
mjr_format = dates.DateFormatter('%m/%d/%Y')
min_format = dates.DateFormatter('%H:%M')

ax.xaxis.set_major_locator(dyloc)
ax.xaxis.set_major_formatter(mjr_format)
plt.setp(ax.xaxis.get_majorticklabels(), rotation = 90)

ax.xaxis.set_minor_locator(hrloc)
ax.xaxis.set_minor_formatter(min_format)
plt.setp(ax.xaxis.get_minorticklabels(), rotation = 90)

plt.subplots_adjust(bottom = 0.25)

# Plot data
ax.plot(dat_time, dat_temp, color = 'c')
fig.savefig('temp_plot.png', facecolor = 'k', edgecolor = 'none')

# HTML output
print "Content-type: text/html; image/png"
print
print """
<html>
        <head>
                <title>
                        Temperature Logger
                </title>
        </head>
        <body bgcolor = #000000>
                <p style="text-align:center;">
                        <font color="white">
                                ECE 331 Project II<br>
                                Temperature Logger<br>
                                Author: Matthew Blanchard<br>
                        </font>
                        <img src="temp_plot.png" alt="Temperature Plot" width="800" height="600"/>
                </p>
        </body>
<html>"""
