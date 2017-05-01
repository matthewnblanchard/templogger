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
        dat_time.append(dates.date2num(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")))
        dat_temp.append(row[1])

# Set plot font
plt.rcParams["font.family"] = "monospace"

# Create plot
fig = plt.figure()
ax = fig.add_subplot(111)

title = plt.title('Temperature Logs')
plt.setp(title, color = 'w')

# Configure plot
ax.set_ylim([0, 35])
ax.set_xlim([dates.date2num(datetime.now()) - 1, dates.date2num(datetime.now())])
ax.set_ylabel('Temperature (Degrees Celsius)')
ax.xaxis.label.set_color('w')
ax.yaxis.label.set_color('w')
ax.set_xlabel('Time/Date')
ax.set_axis_bgcolor('k')
ax.tick_params(color = 'w', labelcolor = 'w')
ax.grid(color = 'w', linestyle = '-', linewidth = 0.5)
ax.spines['bottom'].set_color('w')
ax.spines['top'].set_color('w')
ax.spines['left'].set_color('r')
ax.spines['right'].set_color('r')

# Plot data
ax.plot(dat_time, dat_temp, color = 'c')
fig.savefig('temp_plot.png', facecolor = 'k', edgecolor = 'none')

print "Content-type: text/html; image/png"
print
print """<html>
<head>
<title>Temperature Logger</title>
</head>
<body bgcolor = #000000>
<br>
<p style="text-align:center;">><img src="temp_plot.png" alt="Temperature Plot" width="800" height="600"/></p>
</body>
<html>"""
