'''
Created on 07.02.2017

@author: ak

Collection of visa classes for different HPIB / GPIB / Visa measurment devices. Whith a hole bunch of function I found usefull

Developped and debuged with Python 3.6 32bit on Windows 7/10

Prequisite:
    pyvisa, numpy, matplotlib, scipy, time, string ...
'''

import visa
import time
import numpy as np
import matplotlib.pyplot
import string
from scipy.interpolate import interp1d
import matplotlib.animation as animation
import unittest
from numpy.f2py.auxfuncs import throw_error


class HP856x(object):
    '''
    classdocs
    This class provides an easy interface to the HP856xEC spectrum analyzer. 
    It should also work with with other HP analyzers (untested)
    '''
    def __init__(self, bus, addr):
        ''' 
        Initiate GPIB instance
        '''
        self.visaID = 'GPIB' + str(bus) +'::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()       
        self.instance = self.rm.open_resource(str(self.visaID))

    def commandInstrument(self, command):
        ''' 
        Send a GPIB command to instrument 
        Raises exception if the device is unreachable
        '''
        code = self.instance.write(str(command))
        if '<StatusCode.success: 0>' not in str(code):
            raise Exception("HP856x device did not respond correctly!")
        
    def queryInstrument(self, request):
        ''' 
        Query GPIB Device
        '''
        return(self.instance.query(request))
        
        
    def span(self, spanMHz):
        ''' 
        set frequency span of spectrum analyzer in (float) MHz 
        '''
        self.setSpan = "SP " + str(spanMHz) + "MHZ"
        self.commandInstrument(self.setSpan)
        print(self.setSpan)
        
    def center(self, centerMHz):
        ''' 
        set center frequency of spectrum analyzer in (float) MHz 
        '''
        self.commandInstrument('CF' + str(centerMHz) + 'MHZ')
        
    def reference(self, external):
        ''' 
        set external reference (True) or internal Reference (False), returns INTernal or EXTernal 
        '''
        if external == True:
            self.commandInstrument('FREF EXT')
        else:
            self.commandInstrument('FREF INT')
        return(self.queryInstrument('FREF?'))
    
        
    def getMeasurmentList(self):
        ''' 
        returns 601 frequency measurments as (float) list 
        '''
        #Fill data point string in List
        self.saMeasStr = self.queryInstrument('TRA?')
        self.saMeasList = self.saMeasStr.split(",")
        for i in range(601):
            self.saMeasList[i] = float(self.saMeasList[i])
        return(self.saMeasList)
    
    def showGraph(self):
        '''
        Shows a graph with the current spectrum analyzer measurments 
        '''
        self.list = self.getMeasurmentList()
        xAxis = []
        for i in range(601):
            xAxis.append(i)
        matplotlib.pyplot.scatter(xAxis, self.list, s=1)
        matplotlib.pyplot.plot(xAxis, self.list)
        matplotlib.pyplot.xlabel('Center Frequency +/- 600 Points')
        matplotlib.pyplot.ylabel('Amplitude [dB]')
        matplotlib.pyplot.title('HP8562 SA Measurment')
        matplotlib.pyplot.grid()    
        matplotlib.pyplot.show()
        
    def monitor(self):
        ''' 
        Shows and overdraws measurments from the spectrum analyzer when it updates 
        '''
        xAxis = []
        for i in range(601):
            xAxis.append(i)
          
        self.fig = matplotlib.pyplot.figure()
        
        matplotlib.pyplot.xlabel('Center Frequency +/- 600 Points')
        matplotlib.pyplot.ylabel('Amplitude [dB]')
        matplotlib.pyplot.title('HP8562 SA Measurment')
        matplotlib.pyplot.grid()  
        
        def animate(i):
            self.list = self.getMeasurmentList() 
            matplotlib.pyplot.scatter(xAxis, self.list, s=1)
            matplotlib.pyplot.plot(xAxis, self.list)
        
        self.ani = animation.FuncAnimation(self.fig, animate, interval=10)
        matplotlib.pyplot.show()

        
    '''
    Constructor
    '''


class RSSMTx(object):
    '''
    classdocs
    This class provides an easy interface to the Rohde & Schwarz SMTx series signal senerators 
    It should also work with with other RS signal generators. 
    
    TODO: Only tested and implemented with com. over GPIB port --not RS232
    '''
    def __init__(self, bus, addr):
        ''' 
        Initiate GPIB instance 
        '''
        self.visaID = 'GPIB' + str(bus) +'::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()       
        self.instance = self.rm.open_resource(str(self.visaID))
        self.commandInstrument('*RST; *CLS')

    def commandInstrument(self, command):
        ''' 
        Send a GPIB command to instrument 
        Raises an exception if device unreachable
        '''
        code = self.instance.write(str(command))   
        if '<StatusCode.success: 0>' not in str(code):
            raise Exception("RS SMTx device did not respond correctly!")

        
    def queryInstrument(self, request):
        ''' 
        Query GPIB Device
        '''
        return(self.instance.query(request))  
    
    def rfOff(self, state):
        '''
        Turn of RF output (True) or turn it on (False)
        '''
        if state == True:
            self.commandInstrument('OUTPUT:STATE OFF')
        else:
            self.commandInstrument('OUTPUT:STATE ON')
    
    def setRF(self, frequency, amplitude):
        '''
        Set RF frequency in float MHz and (float) amplitude in dB 
        '''
        self.commandInstrument("FREQ " + str(frequency) +'MHZ' + ": " + "POW" + str(amplitude) + 'DBM')
        
    


        