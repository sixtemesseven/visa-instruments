"""
Created on Thu Dec 13 23:09:20 2018

@author: justRandom

WORK IN PROGRESS 

Goal is to implement OSL cal formula as described in: http://www.hpl.hp.com/hpjournal/94oct/oct94a12.pdf

Short script to load OSL cal data into .txt files @\HP3577_HighZImpeadanceMeas
"""

import numpy as np
import simplevisa #https://github.com/sixtemesseven/visa-instruments

'''
User Settings
'''
startFrequency = 0.1
stopFrequency = 10
BW = 10
sweepTime = 50000 #[ms]

##################################################################################################################
#NO USER EDITS BYOND HERE
##################################################################################################################


'''
Function to get impeadance value - Page 68 Equ. 4
'''
def X(R, A, R0):
    VShunt = np.subtract(R, A)   
    I = np.divide(VShunt, R0)
    return np.divide(A, I)


'''
Setup instrument and get the current meas data to calculate impeadance
'''
vna = simplevisa.HP3577(0,11)
vna.reset()
vna.setSweepTime(sweepTime)
vna.setSweepType(sweepType='log')
vna.setRBW('1HZ')
vna.setImpeadance('R', '1MOhm')
vna.setImpeadance('A', '1MOhm')
vna.setAttenuation('R', '20dB')
vna.setAttenuation('A', '20dB')
vna.setFRQ(startFrequency, stopFrequency)
vna.setSourceAmplitude('10 MV')


print("THIS WILL OVERWRITE YOUR EXISTING OSL CAL VALUES AT \HP3577_HighZImpeadanceMeas")
print("Press any Key to start with OPEN measurment")
input()
vna.doSingleSweep()
R_Open = vna.getDataNP('R')
A_Open = vna.getDataNP('A')

print("Press any Key to start with SHORT measurment")
input()
vna.doSingleSweep()
R_Short = vna.getDataNP('R')
A_Short = vna.getDataNP('A')

print("Press any Key to start with 50OHM_LOAD  measurment")
input()
vna.doSingleSweep()
R_Load = vna.getDataNP('R')
A_Load = vna.getDataNP('A')


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
Zlsi = np.full(400, 49.2+0j) #TODO Zlsi should be the TRUE impeadance for the load standart (Non Ideal resistor so =/= 50+0j of course)


'''
Calculate K Parameters - Page 70 Equ. 5
'''
K1 = np.multiply(np.multiply(A, Zlsi), R0)
K2 = np.divide(np.multiply(arrNeg1, Zsm), R0)
K3 = np.multiply(np.multiply(arrNeg1, Yom), R0)

'''
Save the K cal Parameters to file
'''

np.savetxt('calData\K1.txt', K1.view(float).reshape(-1, 2)) #Save array to file
np.savetxt('calData\K2.txt', K2.view(float).reshape(-1, 2)) #Save array to file
np.savetxt('calData\K3.txt', K3.view(float).reshape(-1, 2)) #Save array to file


print("FINISHED")