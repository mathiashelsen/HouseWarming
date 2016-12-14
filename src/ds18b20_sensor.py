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
