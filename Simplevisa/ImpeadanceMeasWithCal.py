# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:09:20 2018

@author: justRandom
"""

import numpy as np
import simplevisa #https://github.com/sixtemesseven/visa-instruments
import visa
import matplotlib.pyplot as plt


'''
Function to get impeadance value
'''
def X(R, A, R0):
    VShunt = np.subtract(R, A)
    I = np.divide(VShunt, R0)
    return(np.divide(A, I))
    

vna = simplevisa.HP3577(0,11)

R = vna.getDataNP('R')
A = vna.getDataNP('A')


'''
Uncomment those pairs to save new OSL measurments to files for convinience
'''

#np.savetxt('HP3577_HighZImpeadanceMeas\R_Open.txt', R.view(float).reshape(-1, 2)) #Save array to file
#np.savetxt('HP3577_HighZImpeadanceMeas\A_Open.txt', R.view(float).reshape(-1, 2)) #Save array to file

#np.savetxt('HP3577_HighZImpeadanceMeas\R_Short.txt', R.view(float).reshape(-1, 2)) #Save array to file
#np.savetxt('HP3577_HighZImpeadanceMeas\A_Short.txt', R.view(float).reshape(-1, 2)) #Save array to file

#np.savetxt('HP3577_HighZImpeadanceMeas\R_50.txt', R.view(float).reshape(-1, 2)) #Save array to file
#np.savetxt('HP3577_HighZImpeadanceMeas\A_50.txt', R.view(float).reshape(-1, 2)) #Save array to file


'''
Load all the OSL cal parameters from file
'''
R_Open = np.loadtxt('HP3577_HighZImpeadanceMeas\R_Open.txt').view(complex).reshape(-1) #Read array from file
A_Open = np.loadtxt('HP3577_HighZImpeadanceMeas\A_Open.txt').view(complex).reshape(-1) #Read array from file

R_Short = np.loadtxt('HP3577_HighZImpeadanceMeas\R_Short.txt').view(complex).reshape(-1) #Read array from file
A_Short = np.loadtxt('HP3577_HighZImpeadanceMeas\A_Short.txt').view(complex).reshape(-1) #Read array from file

R_Load = np.loadtxt('HP3577_HighZImpeadanceMeas\R_50.txt').view(complex).reshape(-1) #Read array from file
A_Load = np.loadtxt('HP3577_HighZImpeadanceMeas\A_50.txt').view(complex).reshape(-1) #Read array from file


#Parameters used for K calculation
arr1 = np.full(400, 1.0) #Array filled with 1
R0 = np.full(400, 10.0 + 0j) #TODO get real measurments of shunt resistor (Non Ideal)
Zlmi = X(R_Load, A_Load, R0) #Measured impeadance for load standard
Yom = np.divide(arr1, X(R_Open, A_Open, R0)) #Measured admitance for open standard
Zsm = X(R_Short, A_Short, R0) #Measured impeadance for open standard
A = np.divide(np.subtract(arr1, np.multiply(Zlmi, Yom)), np.subtract(Zlmi, Zsm))
Zlsi = X(R_Load, A_Load, R0)

#Calculate K Parameters
K1 = np.multiply(np.multiply(A, Zlsi), R0)
K2 = np.divide(np.negative(Zsm), R0)
K3 = np.divide(np.negative(Yom), R0)

plt.plot(K1)
plt.plot(K2)
plt.plot(K3)
plt.show()

#np.savetxt("R_10Ohm.cvs",R,delimiter=', ')
#np.savetxt("A_10Ohm.cvs",R,delimiter=', ')

#shuntArr = np.full(400, shuntRes)
#
#VShunt = np.subtract(R, A)
#I = np.divide(VShunt, shuntArr)
#result = np.divide(A, I)
#
#absolute = np.absolute(result)  
#plt.plot(absolute)
#plt.show()

