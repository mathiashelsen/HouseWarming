#!/usr/bin/python2.7

import numpy as np
from datetime import datetime

settings = np.genfromtxt('/home/pi/HouseWarming/examples/normal.csv', delimiter=';')
errLog = file('/home/pi/houseWarming.log', 'a')

defTemp = 10.0
hyst = 0.5

errLog.write('# ' + datetime.today() + '\n')
errLog.flush()
