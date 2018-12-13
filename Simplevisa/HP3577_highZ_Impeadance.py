# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 00:20:08 2018

@author: justRandom
"""

import numpy as np
import simplevisa #https://github.com/sixtemesseven/visa-instruments
import visa
import matplotlib.pyplot as plt

shuntRes = 9.962+0j

rm = visa.ResourceManager()
print(rm.list_resources())

vna = simplevisa.HP3577(0,11)

R = vna.getDataNP('R')
A = vna.getDataNP('A')

#np.savetxt("R_10Ohm.cvs",R,delimiter=', ')
#np.savetxt("A_10Ohm.cvs",R,delimiter=', ')

shuntArr = np.full(400, shuntRes)

VShunt = np.subtract(R, A)
I = np.divide(VShunt, shuntArr)
result = np.divide(A, I)

absolute = np.absolute(result)  
plt.plot(absolute)
plt.show()