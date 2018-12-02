import visa
import simplevisa
import time

rm = visa.ResourceManager()
print(rm.list_resources())

vna = simplevisa.HP3577(0,11)


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

'''
vna.getData("A")
vna.plotPolar("R")
'''