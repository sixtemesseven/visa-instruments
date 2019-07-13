#!/usr/bin/env python

import simplevisa as sv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':

    smu236 = sv.Keithley23x(0,29)
    smu238 = sv.Keithley23x(0,30)
    
    #smu2.measureCurrent(0, 0.05)
    
    #smu1.integrationTime(3) #Set Integration time to 20ms
    #smu1.filter(2) #Average Filter
    #plt.plot(smu236.linearVoltageSweep(-3, 3, 0.1, complianceCurrent=0.1, delay=0))
    
    smu236.factoryReset()
    smu238.factoryReset()
    
    smu236.accurateMeasPreset()
    smu238.accurateMeasPreset()
   
    dualSetup = sv.dualSmu(smu236, smu238)
    dualSetup.curveTracerFET(1, 1.5, 0.25, 0.01, 0, 5, 0.05, 1, plot=True, savePlot=True, saveData=True)
    
     
