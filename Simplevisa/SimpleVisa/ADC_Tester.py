# -*- coding: utf-8 -*-
"""
Created on Tue May 29 08:11:47 2018

@author: sixtimesseven
"""

#Uses a HP6632, Rigol Dmm and ADC

points = 100
maxVoltage = 2100

import simplevisa
import time

if __name__ == '__main__':
    VMeter = simplevisa.DM3068("USB0::0x1AB1::0x0C94::DM3O140600028::INSTR")
    PSupply = simplevisa.HPPow(0, 11)  
    PSupply.setOverCurrent(0.2)

    for i in range(points):
        k = i * (maxVoltage / points) / 1000
        PSupply.setVoltage(k)
        print(k)
        for j in range(100):
            time.sleep(1)
            v = VMeter.measureVoltage()
            print(v)
    PSupply.setVoltage(0)

