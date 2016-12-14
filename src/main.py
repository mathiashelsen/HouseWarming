#!/usr/bin/python2.7

# Copyright (c) 2016, Mathias Helsen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or 
# other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

import numpy as np
from datetime import datetime

def getTemp():
    raise IOError('Could not read from temperature sensor')
    return 20.0

def initTempSensor():

settings = np.genfromtxt('/home/pi/HouseWarming/examples/normal.csv', delimiter=',')
errLog = file('/home/pi/houseWarming.log', 'a')

try:
    defaultTemp = 10.0
    hysteresis = 0.5
    calendar = dict()

    currentTemp = defaultTemp
    targetTemp = defaultTemp
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

    print calendar

    while(True):
	currentTemp = getTemp()

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
		    else:
			targetTemp = todaySettings[i][2] - hysteresis

        # Apply control to the CV system
        if( currentTemp > targetTemp ):
	    statusCV = False
        else:
	    statusCV = True

except IOError as e:
    errLog.write('# Error during execution\n')
    errLog.write('# ' + str(datetime.today()) + '\n')
    errStr = "# I/O error({0}): {1}\n".format(e.errno, e.strerror)
    errLog.write(errStr)
    errLog.flush()

    errLog.write('# Trying to halt operation\n')
    statusCV = False
    errLog.write('# End of execution\n')

errLog.flush()
errLog.close()
