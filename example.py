'''
Created on 08.02.2017

@author: ak
'''

from simplevisa import HP856x
from simplevisa import HPPow
from simplevisa import HP3488
from time import sleep


if __name__ == '__main__': 
        
    '''
    switch = HP3488(0, 9)
    switch.write("ID?")
    print(switch.read())
    ''' 
    
    '''
    #Open Power Supplies
    pow1 = HPPow(0, 3)
    pow2 = HPPow(0, 2)

    pow1.setCurrent(0.5)
    pow1.setVoltage(3.4, enable=True)
    
    pow2.setVoltage(5.1, channel=1)
    pow2.setVoltage(5.1, channel=2)
    pow2.setCurrent(1, channel=1)
    pow2.setCurrent(1, channel=2)

    #Open Spectrum Analyzer
    sa = HP856x(0, 18)
    sa.setSpan(1000)
    sa.setCenter(10000)
    #Show Waveforms (accumulative)
    sa.monitor(True)
    '''

    pass

        
