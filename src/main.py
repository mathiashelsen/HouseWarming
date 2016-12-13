#!/usr/bin/python2.7

import numpy as np
from datetime import datetime

settings = np.genfromtxt('/home/pi/HouseWarming/examples/normal.csv', delimiter=';')
errLog = file('/home/pi/houseWarming.log', 'a')

defTemp = 10.0
hyst = 0.5
calendar = dict()

errLog.write('# Script started execution\n')
errLog.write('# ' + str(datetime.today()) + '\n')
errLog.flush()

print settings.shape
if(settings.shape[0] > 2):
    defTemp = settings[0,0]
    hyst = settings[1,0]
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

errLog.flush()
errLog.close()
