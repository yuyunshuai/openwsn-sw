import os
import sys
if __name__=='__main__':
    cur_path = sys.path[0]
    sys.path.insert(0, os.path.join(cur_path, '..', '..'))                     # openvisualizer/
    sys.path.insert(0, os.path.join(cur_path, '..', '..', '..', 'openCli'))    # openCli/

from moteProbe     import moteProbe
from OpenCli       import OpenCli

TCP_PORT_START = 8090

class moteProbeCli(OpenCli):

    def __init__(self,moteProbe_handlers):
        
        # store params
        self.moteProbe_handlers     = moteProbe_handlers
        
        # initialize parent class
        OpenCli.__init__(self,"mote probe CLI",self.quit_cb)
    
    def quit_cb(self):
        
        for mb in self.moteProbe_handlers:
           mb.quit()

def main():
    
    moteProbe_handlers = []

    # create a moteProbe for each mote connected to this computer
    serialPortNames     = moteProbe.utils.findSerialPorts()
    port_numbers        = [TCP_PORT_START+i for i in range(len(serialPortNames))]
    for (serialPortName,port_number) in zip(serialPortNames,port_numbers):
        moteProbe_handlers.append(moteProbe.moteProbe(serialPortName,port_number))

    # create an open CLI
    cli = moteProbeCli(moteProbe_handlers)
    cli.start()

#============================ application logging =============================
import logging
import logging.handlers
logHandler = logging.handlers.RotatingFileHandler('moteProbe.log',
                                                  maxBytes=2000000,
                                                  backupCount=5,
                                                  mode='w')
logHandler.setFormatter(logging.Formatter("%(asctime)s [%(name)s:%(levelname)s] %(message)s"))
for loggerName in ['moteProbe',
                   'moteProbeSerialThread',
                   'moteProbeSocketThread',
                   'moteProbeUtils',
                   ]:
    temp = logging.getLogger(loggerName)
    temp.setLevel(logging.DEBUG)
    temp.addHandler(logHandler)
    
if __name__=="__main__":
    main()