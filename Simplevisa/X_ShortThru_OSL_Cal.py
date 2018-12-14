# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:09:20 2018

@author: justRandom

WORK IN PROGRESS 

Goal is to implement OSL cal formula as described in: http://www.hpl.hp.com/hpjournal/94oct/oct94a12.pdf
Please Run \Get_OSL_Cal.py first to get the cal values saved...

TODO: Move all the Kx calculations to the Get_OSL_Cal file were they belong...
TODO: Pack the fun defs somwhere nicer...
"""

import numpy as np
import simplevisa #https://github.com/sixtemesseven/visa-instruments
import matplotlib.pyplot as plt


'''
Function to get impeadance value - Page 68 Equ. 4
'''
def X(R, A, R0):
    VShunt = np.subtract(R, A)   
    I = np.divide(VShunt, R0)
    return np.divide(A, I)


'''
Function to calculate impeadance - Page 67 Equ. 1
'''
def Xcal(K1, K2, K3, R, A, R0):
    arr1 = np.full(400, 1.0) #Array filled with 1
    V1 = np.subtract(R, A)
    V2 = A
    Vr = np.divide(V2, V1)
    Zx = np.multiply(K1, np.divide(np.add(K2, Vr), np.add(arr1, np.multiply(K3, Vr))))
    return Zx


'''
Load all the OSL cal parameters from file - You can get them by executing Save_OSL.py first
'''
R_Open = np.loadtxt('HP3577_HighZImpeadanceMeas\R_Open.txt').view(complex).reshape(-1) #Read array from file
A_Open = np.loadtxt('HP3577_HighZImpeadanceMeas\A_Open.txt').view(complex).reshape(-1) #Read array from file
R_Short = np.loadtxt('HP3577_HighZImpeadanceMeas\R_Short.txt').view(complex).reshape(-1) #Read array from file
A_Short = np.loadtxt('HP3577_HighZImpeadanceMeas\A_Short.txt').view(complex).reshape(-1) #Read array from file
R_Load = np.loadtxt('HP3577_HighZImpeadanceMeas\R_50.txt').view(complex).reshape(-1) #Read array from file
A_Load = np.loadtxt('HP3577_HighZImpeadanceMeas\A_50.txt').view(complex).reshape(-1) #Read array from file


'''
Parameters used for K calculation - Page 70 Equ. 5
'''
arr1 = np.full(400, 1) #Array filled with 1
arrNeg1 = np.full(400, 1) #Array filled with -1
R0 = np.full(400, 10.0 + 0j) #TODO get real measurments of shunt resistor (Non Ideal resistor so =/= 10+0j of course)
Zlmi = X(R_Load, A_Load, R0) #Measured impeadance for load standard
Yom = np.reciprocal(X(R_Open, A_Open, R0)) #Measured admitance for open standard
Zsm = X(R_Short, A_Short, R0) #Measured impeadance for open standard
A = np.divide(np.subtract(arr1, np.multiply(Zlmi, Yom)), np.subtract(Zlmi, Zsm))
Zlsi = np.full(400, 50+0j) #TODO Zlsi should be the TRUE impeadance for the load standart (Non Ideal resistor so =/= 50+0j of course)


'''
Calculate K Parameters - Page 70 Equ. 5
'''
K1 = np.multiply(np.multiply(A, Zlsi), R0)
K2 = np.divide(np.multiply(arrNeg1, Zsm), R0)
K3 = np.multiply(np.multiply(arrNeg1, Yom), R0)


'''
Get the current meas data to calculate impeadance
'''
vna = simplevisa.HP3577(0,11)
R = vna.getDataNP('R')
A = vna.getDataNP('A')


''' 
Plot Resulting Impeadance
'''
plt.plot(np.absolute(Xcal(K1, K2, K3, R, A, R0)))
plt.show()




