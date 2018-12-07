import time
import numpy as np
from skrf import Network
import simplevisa
import visa
import matplotlib.pyplot as plt
import operator


rm = visa.ResourceManager()
print(rm.list_resources())


vna = simplevisa.HP3577(0,11)

print('Start short cal [y]')
x = input()

if(x=='y'):
    refR = vna.getData('R')
    refA = vna.getData('A')
    refB = vna.getData('B')
    
    print('Start measurment [y]')
    z = input()
    
    if(z == 'y'):
        R =  vna.getData('R')
        map(operator.sub, R, refR)
        plt.plot(R)
    
    
    
    
    







'''
sta = 0.1
sto = 20
nos = 401 

net = vna.put1Network('R', 0.1, 10)


#net.plot_s_smith()

net.plot_s_deg_unwrap()
net.plot_s_db()

#net.plot_s_db()




vna.setFRQ(sta, sto)
data = vna.getData('R')

print('Frequency [MHz], real [mV], imaginary [mV]')

for i in range(0, nos-1):
    sampleFrequency = sta + (step * i)
    if(sampleFrequency == 0.1):
        print(str(sampleFrequency) + ', ' + str(data[i].real) + ', ' + str(data[i].imag) + '\r\n')


#print(vna.getSinglePoint('R', 1, 1000))


vna.setSweep(1000, sweepMode='continious', sweepType='linear')
print(vna.sweepComplete())
print(bin(vna.getStatusByte()))
time.sleep(2)
print(vna.sweepComplete())
print(bin(vna.getStatusByte()))
vna.plotMagdBm('R')


#vna.plotMag('R')fdfd
#vna.plotMagdBm('R')

#vna.plotPolar("R")
#vna.getData("A")

vna.getData("A")
vna.plotPolar("R")
'''

