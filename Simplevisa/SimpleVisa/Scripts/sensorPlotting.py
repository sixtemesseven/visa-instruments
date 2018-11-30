# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:05:13 2018

@author: justRandom
"""

import matplotlib.pyplot as plt

P = 6e-5        #Nominal Power consumtion in W
C = 0.114       #Capacity C
U0 = 5          #Start Voltage V
U1 = 3.14       #Lowest Voltage V
timeStep = 1    #TimeStep in s

Q = C * U0
I = 0  
it = []
ut = []

while(U0 > U1):
    currentTakenInStep = (P / U0) * timeStep
    it.append(currentTakenInStep)
    Q = Q - currentTakenInStep
    U0 = Q / C
    ut.append(U0)

plt.subplot(2,1,1)
plt.plot(ut)
plt.subplot(2,1,2)
plt.plot(it)



    
