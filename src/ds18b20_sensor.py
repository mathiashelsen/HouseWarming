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
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from subprocess import check_output 

class ds18b20_sensor:
    def __init__(self, verbose=False, tries=10, delay=0.5):
        initialized = False
        self.address = ''
        self.tries = tries 
        self.delay = delay
        self.verbose=verbose

    def initialize(self):
        lsOut = str(check_output('ls -l /sys/bus/w1/devices/', shell=True))
        if(self.verbose):
            print '# Output from searching for 1-wire devices:'
            print lsOut


        lowerIndex = lsOut.find('28-00000')
        if( lowerIndex == -1 ):
            raise IOError()
        else:
            upperIndex = lowerIndex + 6
            self.address = '/sys/bus/w1/devices/' + lsOut[lowerIndex:upperIndex]
            self.initialized = True
            
        if(self.verbose):
            print "# Found device, will be using address: ", self.address

    def readRaw(self):
        f = open(self.address, 'r')
        lines = f.readlines()
        f.close()
        return lines
 
    def readTemp(self):
        if(not self.initialized):
            self.initialize()

        lines = self.readRaw()
        if(self.verbose):
            print "# Read from 1-wire bus: "
            print lines

        currentTry = 1
        while (lines[0].strip()[-3:] != 'YES' and currentTry < self.tries):
            time.sleep(self.delay)
            lines = self.readRaw()
            if(self.verbose):
                print "# Currently at try: ", currentTry
                print "# Read from 1-wire bus: "
                print lines

            currentTry = currentTry + 1

        if(lines[0].strip()[-3:] != 'YES'):
            raise IOError()

        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            if(self.verbose):
                print "# Read temperature to be: ", temp_c

            return temp_c
        else:
            raise IOError()
