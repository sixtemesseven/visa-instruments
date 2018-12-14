"""
Created on Thu Dec 13 23:09:20 2018

@author: justRandom

Short script to load OSL cal data into .txt files @\HP3577_HighZImpeadanceMeas
"""

import numpy as np
import simplevisa #https://github.com/sixtemesseven/visa-instruments


    
vna = simplevisa.HP3577(0,11)


print("THIS WILL OVERWRITE YOUR EXISTING OSL CAL VALUES AT \HP3577_HighZImpeadanceMeas")
print("Press any Key to start with OPEN measurment")
input()
R = vna.getDataNP('R')
A = vna.getDataNP('A')
np.savetxt('HP3577_HighZImpeadanceMeas\R_Open.txt', R.view(float).reshape(-1, 2)) #Save array to file
np.savetxt('HP3577_HighZImpeadanceMeas\A_Open.txt', A.view(float).reshape(-1, 2)) #Save array to file

print("Press any Key to start with SHORT measurment")
input()
R = vna.getDataNP('R')
A = vna.getDataNP('A')
np.savetxt('HP3577_HighZImpeadanceMeas\R_Short.txt', R.view(float).reshape(-1, 2)) #Save array to file
np.savetxt('HP3577_HighZImpeadanceMeas\A_Short.txt', A.view(float).reshape(-1, 2)) #Save array to file

print("Press any Key to start with 50OHM_LOAD  measurment")
input()
R = vna.getDataNP('R')
A = vna.getDataNP('A')
np.savetxt('HP3577_HighZImpeadanceMeas\R_50.txt', R.view(float).reshape(-1, 2)) #Save array to file
np.savetxt('HP3577_HighZImpeadanceMeas\A_50.txt', A.view(float).reshape(-1, 2)) #Save array to file

print("FINISHED")