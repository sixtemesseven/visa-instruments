'''
Created on Jul 2, 2017

@author: sixtimesseven
'''

import simplevisa 
import numpy as np
import matplotlib.pyplot as plt

HP663xAddr = 3
GPIBPort = 0
DM3068Addr = "USB0::0x1AB1::0x0C94::DM3O140600028::INSTR"

FileName = input("Input File Name for CSV Output File")
mode = input("1 = VC Mode, 2 = CC Mode")
settleTime = input("Settle time before taking measurment [ms]")
startmeasurement = input("Input Start voltage [V]")
stopmeasurement = input("Input Stop voltage [V]")
stepSize = input("Step Size [V]")

if __name__ == '__main__':
    
    HP336x = HPPow(GPIBPort, HP663xAddr)
    DMM = DM3068(DM3068Addr)

    t = np.arange(startmeasurement, stopmeasurement, stepSize)
    N = len(t)
    measurement = []
    i = N
    
    for index in range(N):
        print(t[N - i])
        if mode is 1:
            HP336x.setvoltage(t[i], enable=True)
            time.sleep(settleTime)
            measurement.append(float(DMM.measurevoltage())) 
        if mode is 2:
            HP336x.setCurrent(t[i], enable=True)
            time.sleep(settleTime)
            measurement.append(float(DMM.measurecurrent())) 
        else:
            print("Error: Mode not Specified")
            pass

        print(measurement) 
        i = i-1
        
    FileName = FileName + ".csv"
                
    f = open(FileName, "w")
    for i in range(len(t)):
        f.write("{} {}\n".format(t[i], measurement[i]))
    f.close()
        
    plt.plot(t, measurement)
    plt.show()
    
    pass