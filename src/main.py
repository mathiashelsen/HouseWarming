#!/usr/bin/python2.7

import numpy as np
from datetime import datetime

settings = np.genfromtxt('/home/pi/HouseWarming/examples/normal.csv', delimiter=';')
errLog = file('/home/pi/houseWarming.log', 'a')

defaultTemp = 10.0
hysteresis = 0.5
calendar = dict()

currentTemp = 21.0
targetTemp = defTemp
statusCV = False

errLog.write('# Script started execution\n')
errLog.write('# ' + str(datetime.today()) + '\n')
errLog.flush()

print settings.shape
if(settings.shape[0] > 2):
    defaultTemp = settings[0,0]
    hysteris = settings[1,0]
    for i in range(2,settings.shape[0]):
	day = settings[i,0]
	start = settings[i,1]
	stop = settings[i,2]
	setpoint = settings[i,3]
	if day in calendar.keys():
	    calendar[day].append([start, stop, setpoint])
	else:
	    calendar[day] = [[start, stop, setpoint]]
else:
    errLog.write('# Insufficient settings provided\n')
    errLog.flush()

print defTemp, hyst
print calendar

while(True):
    # Set default temperature as fallback
    if(statusCV):
	targetTemp = defaultTemp + hysteresis
    else:
	targetTemp = defaultTemp - hysteresis

    # Look up the settings for today
    if datetime.today().weekday() in calendar.keys():
	todaySettings = calendar[datetime.today().weekday()]
	time = datetime.today().hour + datetime.today().minute/60.0

	# Find the slot in which we are
	for i in range(len(todaySettings)):
	    if( time >= todaySettings[i][0] and time < todaySettings[i][1]):
		if(statusCV):
		    targetTemp = todaySettings[i][2] + hysteresis
		else(statusCV):
		    targetTemp = todaySettings[i][2] - hysteresis

	print todaySettings
	print targetTemp

    # Apply control to the CV system
    if( currentTemp > targetTemp ):
	statusCV = False
	# CV Off
    else:
	statusCV = True
	# CV On

errLog.flush()
errLog.close()
