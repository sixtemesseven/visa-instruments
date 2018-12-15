# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:09:20 2018

@author: justRandom

WORK IN PROGRESS 

Goal is to implement OSL cal formula as described in: http://www.hpl.hp.com/hpjournal/94oct/oct94a12.pdf
Please Run \Get_OSL_Cal.py first to get the cal values saved...

TODO: Pack the fun defs somwhere better...
TODO: Save K values into sub-folder
"""

import numpy as np
import simplevisa #https://github.com/sixtemesseven/visa-instruments
import matplotlib.pyplot as plt


'''
User Settings
'''
startFrequency = 1000
stopFrequency = 10000000
BW = 10
SweepTime = 50


'''
Function to calculate impeadance - Page 67 Equ. 1
'''
def Xcal(K1, K2, K3, R, A):
    arr1 = np.full(400, 1.0) #Array filled with 1
    V1 = np.subtract(R, A)
    V2 = A
    Vr = np.divide(V2, V1)
    Zx = np.multiply(K1, np.divide(np.add(K2, Vr), np.add(arr1, np.multiply(K3, Vr))))
    return Zx


'''
Load all the OSL cal K parameters from file - You can get them by executing Save_OSL.py first
'''
K1 = np.loadtxt('HP3577_HighZImpeadanceMeas\K1.txt').view(complex).reshape(-1) #Read array from file
K2 = np.loadtxt('HP3577_HighZImpeadanceMeas\K2.txt').view(complex).reshape(-1) #Read array from file
K3 = np.loadtxt('HP3577_HighZImpeadanceMeas\K3.txt').view(complex).reshape(-1) #Read array from file


'''
Get the current meas data to calculate impeadance
'''
vna = simplevisa.HP3577(0,11)
R = vna.getDataNP('R')
A = vna.getDataNP('A')


''' 
Plot Resulting Impeadance
'''
fStep = (stopFrequency - startFrequency) / (400)
yAxis = np.arange(startFrequency, stopFrequency, fStep)
Xdut = Xcal(K1, K2, K3, R, A)
plt.plot(yAxis, np.absolute(Xdut))
plt.plot(yAxis, np.angle(Xdut))
plt.show()




