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
            raise Exception("Device did not respond correctly!")
        
        
    def queryInstrument(self, request):
        ''' 
        Query GPIB Device
        '''
        return(self.instance.query(str(request)))
        
        
    def setSpan(self, spanMHz):
        ''' 
        set frequency span of spectrum analyzer in (float) MHz 
        '''
        self.setSpan = "SP " + str(spanMHz) + "MHZ"
        self.commandInstrument(self.setSpan)
        print(self.setSpan)
       
        
    def setCenter(self, centerMHz):
        ''' 
        set center frequency of spectrum analyzer in (float) MHz 
        '''
        self.commandInstrument('CF' + str(centerMHz) + 'MHZ')
     
        
    def setExternalRef(self, external=None):
        ''' 
        set external reference (True) or internal Reference (False), returns INTernal or EXTernal 
        '''
        if external is None:
            external = True
        if external == True:
            self.commandInstrument('FREF EXT')
        else:
            self.commandInstrument('FREF INT')
        return(self.queryInstrument('FREF?'))
    
    def setRBW(self, RBW=None):
        ''' 
        Set resolution bandwith manual in MHz or to auto rbw (float) (default=Auto)
        '''
        if RBW is None:
            self.commandInstrument('RB AUTO')
        else:
            self.commandInstrument('RB' + RBW + 'MHZ')
            
    def setTitle(self, text):
        ''' 
        Writes a title on top of the sa display and vga output
        '''
        self.commandInstrument('TITLE' + text)

    def getMarker(self, text):
        ''' 
        Writes a title on top of the sa display and vga output
        '''
        self.commandInstrument('TITLE' + text)
            
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
     
        
    def monitor(self, persistance=None):
        ''' 
        Shows and overdraws measurments from the spectrum analyzer as it updates 
        
        Keywords:
        persistance = overlays graphs continiously when on (bool) (Default=OFF)
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
            if persistance is None:
                matplotlib.pyplot.clf()
            self.list = self.getMeasurmentList() 
            matplotlib.pyplot.scatter(xAxis, self.list, s=1)
            self.line = matplotlib.pyplot.plot(xAxis, self.list) 
                        
        self.ani = animation.FuncAnimation(self.fig, animate, interval=10)
        matplotlib.pyplot.show()


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
        return(self.instance.query(str(request)))  
    
    def outOff(self, state):
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
        
    
class HP3488(object):
    '''
    classdocs
    This class provides an easy interface to the HP3488 Switch module 
    It should also work with with other RS signal generators. 
    
    TODO: 
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
            raise Exception("RS HP3488 device did not respond correctly!")
        
    def queryInstrument(self, request):
        ''' 
        Query GPIB Device
        '''
        return(self.instance.query(request))
        
    def writeRelay(self, module, relay, state):
        ''' 
        Sets relay to open or closed
        '''
        
    def writeIO(self, module, relay, state):
        ''' 
        Sets relay to open or closed
        '''
        
    def readIO(self, module, relay, state):
        ''' 
        Sets relay to open or close
        '''
    
    
class HPPow(object):
    '''
    Control HP/Agilent Power supplies
    Confirmed working:
        - HP6632A
        - HP6622A (specify channel)
    '''
    
    def __init__(self, bus, addr):
        ''' 
        Initiate GPIB instance 
        
        Keyword Arguments:
        bus -- gpib bus number
        addr -- device Adress
        '''
        self.visaID = 'GPIB' + str(bus) +'::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()       
        self.instance = self.rm.open_resource(str(self.visaID))
        self.commandInstrument('*RST; *CLS; STATus:PRESet; *SRE 0; *ESE 0; RST; CLR')

    def commandInstrument(self, command):
        ''' 
        Send a GPIB command to instrument 
        Raises an exception if device unreachable
        '''
        code = self.instance.write(str(command))   
        if '<StatusCode.success: 0>' not in str(code):
            raise Exception("Device did not respond correctly!")
        
    def queryInstrument(self, request):
        ''' 
        Query GPIB Device
        '''
        return(self.instance.query(str(request)))
    
        
    def setVoltage(self, voltage, channel=None, enable=True):
        ''' 
        Set voltage (float)
        
        Keywords:
        voltage -- Set Voltage (float)
        channel -- Channel Number, do not use if dev. has one channel only (default:None)
        enable -- enable output (bool) (default is ON / Last device state)
        
        Return: 
        Voltage (float)
        '''
        #Check if instrument output is disabled and if so keep it disabled unsless user enables it
        if self.queryInstrument('OUT') is 0 and enable is None:
            enable = False;
        if enable is False:
            self.commandInstrument('OUT 0')
        else:
            self.commandInstrument('OUT 1')
        #Set channel if instrument has more than one channel
        if channel is None:
            self.commandInstrument('VSET' + str(voltage))
        else:
            self.commandInstrument('VSET' + str(channel) + ',' + str(voltage))
        #Return the current output
        return self.queryInstrument('VOUT?')
    
        
    def setCurrent(self, current, channel=None, enable=None):
        ''' 
        Sets the devices Current
        
        Keywords:
        current (float)
        channel -- Channel Number, do not use if dev. has one channel only (default:None)
        enable -- enable output (bool) (default is ON / last device state)
        
        Return current (float)
        
        
        Set channel only if instruments has more than one channel!!!
        '''
        #Check if instrument output is disabled and if so keep it disabled unsless user enables it
        if self.queryInstrument('OUT') is 0 and enable is None:
            enable = False;
        if enable is False:
            self.commandInstrument('OUT 0')
        else:
            self.commandInstrument('OUT 1')
        #Set channel if instrument has more than one channel
        if channel is None:
            self.commandInstrument('ISET' + str(current))
        else:
            self.commandInstrument('ISET' + str(channel) + ',' + str(current))
        #Return the current output
        return self.queryInstrument('IOUT?')
    
    
    def setOverCurrent(self, enable, channel=None):
        ''' 
        Sets overcurrent Protection
        
        Keywords:
        enable = Overcurrent protection on/off bool
        channel = channel number

        Set channel only if instruments has more than one channel!!!
        '''
        if channel is None:
            self.commandInstrument('OCP' + str(int(enable)))
        else:
            self.commandInstrument('ISET' + channel + ',' + int(enable))
            
    def setOverVoltate(self, voltage, channel=None):
        ''' 
        Sets overcurrent Protection
        
        Keywords:
        voltage = Overvoltage (V)
        channel = channel number (default=None for single channel instruments)

        Set channel only if instruments has more than one channel!!!
        '''
        if channel is None:
            self.commandInstrument('OVSET' + voltage)
        else:
            self.commandInstrument('OVSET' + channel + ',' + voltage)
            
    
    
    def setUP(self, current, voltage, channel=None, enable=None, ocp=False, ovp=0):
        ''' 
        Sets most important device parameters
        
        Keywords:
        current (float)
        voltage (float)
        channel -- Channel Number, do not use if dev. has one channel only (default:None)
        enable -- enable output (bool) (default is ON / last device state)
        ocp --- Set overcurrent protection (bool) (default is OFF)
        ovp --- Overvoltage protection (default=0V)

        Set channel only if instruments has more than one channel!!!
        '''
        self.setCurrent(current, channel=channel, enable=enable)
        self.setVoltage(voltage, channel=channel, enable=enable)
        self.setOverCurrent(ocp, channel=channel)
        self.setOverVoltate(ovp, channel=channel)
        
    
class DM3068(object):
    '''
    Control Rigol Multimeter DM3068
    Confirmed working:
    '''
    
    def __init__(self, USB):
        ''' 
        Initiate GPIB instance
        '''
        self.rm = visa.ResourceManager()       
        self.instance = self.rm.open_resource(str(USB))
        self.timeout = 250000


    def commandInstrument(self, command):
        ''' 
        Send a GPIB command to instrument 
        Raises exception if the device is unreachable
        '''
        code = self.instance.write(str(command))
        if '<StatusCode.success: 0>' not in str(code):
            raise Exception("Device did not respond correctly!")
        
        
    def queryInstrument(self, request):
        ''' 
        Query GPIB Device
        '''
        return(self.instance.query(str(request)))
    
    def checkInstrument(self):
        '''
        Return: 
        Voltage (float)
        '''
        self.commandInstrument('*RST')
        self.commandInstrument('*CLS')
        self.commandInstrument('*WAIT')
        print(self.queryInstrument('*IDN?'))
        return
    
        
    def measureVoltage(self):
        '''       
        Return: 
        Voltage (float)
        '''
        self.commandInstrument('CMDSET AGILENT')
        v = self.queryInstrument('MEASure:Voltage:DC?')
        return v 


    
   

        