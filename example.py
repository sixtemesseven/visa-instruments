'''
Created on 08.02.2017

@author: ak
'''

import simplevisa

if __name__ == '__main__':
    


    if __name__ == '__main__':
        
        gen = simplevisa.RSSMTx(0, 28)
        gen.setRF(1000, 0)
        gen.outOff(False)
        
        sa = simplevisa.HP856x(0, 18)
        sa.setSpan(1)
        sa.setCenter(1000)
        sa.monitor()
        
        
        
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
