# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 23:50:13 2019

@author: justRandom

Calculate the accuracy of the Keithley 236 for res. measurments
"""

from uncertainties import ufloat
import numpy as np
import simplevisa as sv

smu236 = sv.Keithley23x(0,29)
smu236.accurateMeasPreset()

voltageSourced = 0.00001 # [V]
ufloat_voltageSourced = ufloat(voltageSourced, voltageSourced*0.00033+6.5e-8)


currentMeasured = smu236.voltageSource(voltageSourced, 0.1)

#Find Current Uncertenty according to Spec
# 1nA Range
if currentMeasured >= 0 and currentMeasured < 1e-9:
    IUncert = currentMeasured * 0.003 + 450 * 10e-15
#TODO insert rest of ranges here    
#TODO insert rest of ranges here
#TODO insert rest of ranges here   
# 1mA Range   
if currentMeasured > 0.0001 and currentMeasured <= 0.001:
    IUncert = currentMeasured * 0.0005 + 2* 10e-8
#10mA Range    
if currentMeasured > 0.001 and currentMeasured <= 0.01:
    IUncert = currentMeasured * 0.0005 + 2 * 10e-6
# 100mA Range   
if currentMeasured > 0.010 and currentMeasured <= 0.1:
    IUncert = currentMeasured * 0.001 + 2 * 10e-5
# 1A Range   
if currentMeasured > 0.10 and currentMeasured <= 1:
    IUncert = currentMeasured * 0.0012 + 7 * 10e-6
    
    
    
    
    
ufloat_currentMeasured = ufloat(currentMeasured, IUncert)


R = ufloat_voltageSourced / ufloat_currentMeasured
tolerance = (1 - ((R.nominal_value - R.std_dev) / (R.nominal_value + R.std_dev)))*100
print("Resistance: %4.3f with a tolerance of: %4.2f %%" %(R.nominal_value, tolerance))

