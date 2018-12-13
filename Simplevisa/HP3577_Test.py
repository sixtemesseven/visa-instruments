import numpy as np
import simplevisa
import visa
import matplotlib.pyplot as plt



inputAmplitude = 0.040 #[V]
shuntRes = 9.962+0j


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
        
        R = np.add(vna.getDataNP('R'), refR)
        V = np.add(vna.getDataNP('A'), refA)      
        
        shuntArr = np.full(400, shuntRes)
        
        VShunt = np.subtract(R, V) 
        I = np.divide(VShunt, shuntArr)
        result = np.divide(V, I)

        absolute = np.absolute(result)  
        plt.plot(absolute)
        plt.show()
    
                    




