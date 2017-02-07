'''
Created on 06.02.2017

@author: ak
'''

import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import string
from scipy.interpolate import interp1d

'''
###HP3488A Test
#Open Relay Command for HP3488A module and channel
def openRC(module, channel):
    return(str('open'.ljust(6) + str(module) + '0' + str(channel)))

#Close Relay Command for HP3488A module and channel
def closeRC(module, channel):
    return(str('close'.ljust(6) + str(module) + '0' + str(channel)))
'''

'''
###HP6632A Test
#Enables / Disables HP6632A output if stat equals TRUE / FALSE
def setOutput(stat):
    if stat == True:
        return(str('OUTPut ON'))
    else:
        return(str('OUTPut OFF'))
    
def setVoltage(volt):
    return(str('VOLTage'.ljust(8) + str(volt)))

def setCurrent(current):
    return(str('CURRent'.ljust(8) + str(current)))
'''


import simplevisa

if __name__ == '__main__':
    
    gen = simplevisa.RSSMTx(0, 28)
    gen.setRF(100, 0)
    
    
    '''    
    ##Switch Example
    #HP3488A0 = rm.open_resource('GPIB0::09::INSTR')
    
    ##Power Supply Exampe
    #HP6632A = rm.open_resource('GPIB0::5::INSTR')
    #HP6632A.write('CSET 1')
    #HP6632A.write('VSET 9')
    #print(HP6632A.query('VOUT?'))
    '''
    
    pass


