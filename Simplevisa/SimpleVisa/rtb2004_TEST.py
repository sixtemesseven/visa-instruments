# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 21:40:21 2018

@author: sixtimesseven
"""

import visa
import matplotlib.pyplot as plt
import numpy



##USER Variables
stopFrequency = 100 

rm = visa.ResourceManager()
print(rm.list_resources())
my_instrument = rm.open_resource('TCPIP::192.168.50.3::INSTR')
print(my_instrument.query('*IDN?'))

#Stop accuistion
my_instrument.write('STOP')

#Set number of Data Points
my_instrument.write('CHANnel1:DATA:POINts MAXimum')

#Get the Data setup for the cannel
#RTB2004 Manual page 366
ch1DataS = my_instrument.query('CHANnel1:DATA:HEADer?')
ch1DataS = ch1DataS.split(",")
ch1DataS = list(map(float, ch1DataS))
ch1StartTime = ch1DataS[0]
ch1StopTime = ch1DataS[1]
ch1RecordLength = ch1DataS[2]
ch1NumberOfValuesPerSample = int(ch1DataS[2])

#Get a single shot
#my_instrument.write('Single')
#time.sleep(1)

#Get Data from RTB200x
ch1Data = my_instrument.query('CHAN1:DATA?')

#Get back to continioue Accuisition
#my_instrument.write('RUN')

#Get Data Format right
ch1Data = ch1Data.replace('"','');
ch1Data = ch1Data.replace(' ','');
ch1Data = ch1Data.replace('ins,C1inV','')
ch1Data = ch1Data.replace('\r\n',',')
ch1Data = ch1Data[:-2]
ch1Data = ch1Data.split(',')
ch1Data.pop(0)
ch1Data.pop(0)

#Split into a timestamp and a measurment array
timeStamp = list()
measurment = list()
c = 0
for i in range(ch1NumberOfValuesPerSample):
    timeStamp.append(float(ch1Data[c]))
    measurment.append(float(ch1Data[c+1]))
    c = c + 2

#Calculate fft xAxis
dt = (timeStamp[ch1NumberOfValuesPerSample-1] - timeStamp[0]) / ch1NumberOfValuesPerSample
maxF = int(1/dt)
t = list()
  
#Calculate and fft
fftData = numpy.fft.rfft(measurment)
fftData = numpy.asarray(fftData)
fftR = numpy.real(fftData)
fftC = numpy.real(fftData)
fftData = numpy.power( (numpy.sqrt(numpy.power(fftR, 2) + numpy.power(fftC, 2))), 2)


#Calculate xAxis Frequencies to plot xAxis  
t = numpy.fft.rfftfreq(ch1NumberOfValuesPerSample, dt)

#Get max frequency value to plot
maxT = 0
while 1:
    if(t[maxT] >= stopFrequency):
        break
    maxT = maxT + 1
    
#Plot FFT data
plt.plot(t[1:maxT], fftData[1:maxT])

