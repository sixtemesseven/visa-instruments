import numpy as np
import simplevisa
import visa
import matplotlib.pyplot as plt



inputAmplitude = 0.020 #[V]
rm = visa.ResourceManager()
print(rm.list_resources())

vna = simplevisa.HP3577(0,11)

print('Start short cal, type ENTER')
x = input()

R0 = vna.getDataNP('R')
A0 = vna.getDataNP('A')

ampt = np.full(400, inputAmplitude+0j)
refR = np.subtract(ampt, R0)
refA = np.subtract(ampt, A0) 

plt.plot(refR)
plt.plot(refA)
plt.show()
  

while(True):
        print('Start new measurment type: ENTER, stop measurments type "end"')
        x = input()
        
        if(x == 'end'): 
            break
        
        R = np.add(np.asarray(vna.getData('R')), refR)
        A = np.add(np.asarray(vna.getData('A')), refA)
        
        
        arr10 = np.full(400, 10+0j)
        absolute = np.full(400, 0)
        
        VShunt = np.subtract(R, A)
        result = np.subtract(np.divide(np.multiply(arr10, R), VShunt), arr10)
        absolute = np.absolute(result)  
        plt.plot(absolute)
        plt.show()
        

sas
            
                    




