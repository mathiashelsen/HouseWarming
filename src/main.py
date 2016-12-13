#!/usr/bin/python2.7

import numpy as np
from datetime import datetime

settings = np.genfromtxt('/home/pi/HouseWarming/examples/normal.csv', delimiter=';')
errLog = file('/home/pi/houseWarming.log', 'a')

defTemp = 10.0
hyst = 0.5

errLog.write('# Script started execution\n')
errLog.write('# ' + str(datetime.today()) + '\n')
errLog.flush()

if(settings.shape[1] > 2):
    defTemp = settings[0,0]
    hyst = settings[1,0]
else:
    errLog.write('# Insufficient settings provided\n')
    errLog.flush()

print defTemp, hyst

errLog.flush()
errLog.close()
