#!/usr/bin/python2.7

import numpy as np
from datetime import date

settings = np.genfromtxt('../examples/normal.csv', delimiter=';')
errLog = file('/home/pi/houseWarming.err', 'a')

defTemp = 10.0
hyst = 0.5

print date.today

try:
    # Try to construct the dictionary
    if(settings.shape[1] < 3):
	print "not enough settings provided"
    for i in range(settings.shape[1]-2):
	    
