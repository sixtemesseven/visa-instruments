#!/usr/bin/env python

import simplevisa
import matplotlib.pyplot as plt

if __name__ == '__main__':

    smu1 = simplevisa.Keithley23x(0,29)
    smu2 = simplevisa.Keithley23x(0,30)
    
    smu1.integrationTime(3) #Set Integration time to 20ms
    smu1.filter(2) #Average Filter
    plt.plot(smu1.linearVoltageSweep(-4, 4, 0.1, complianceCurrent=0.05, delay=0))




