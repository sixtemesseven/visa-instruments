'''
Created on 07.02.2017

@author: ak

Collection of visa classes for different HPIB / GPIB / Visa measurment devices. Whith a hole bunch of function I found usefull

Developped and debuged with Python 3.6 32bit on Windows 7/10

Prequisite:
    pyvisa, numpy, matplotlib, scipy, time, string ...
'''

import visa
import numpy as np
import matplotlib.pyplot as plt
import string
import math
import cmath
import time
from skrf import Network, Frequency

        
        
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
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
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
        if external:
            self.commandInstrument('FREF EXT')
        else:
            self.commandInstrument('FREF INT')
        return(self.queryInstrument('FREF?'))

    def setRBW(self, RBW=None):
        '''
        Set resolution bandwith manual in MHz or to auto rbw (float) (default=Auto)
        '''
        if RBW is not None:
            self.commandInstrument('RB' + RBW + 'MHZ')
        else:
            self.commandInstrument('RB AUTO')

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
        # Fill data point string in List
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
        plt.scatter(xAxis, self.list, s=1)
        plt.plot(xAxis, self.list)
        plt.xlabel('Center Frequency +/- 600 Points')
        plt.ylabel('Amplitude [dB]')
        plt.title('HP8562 SA Measurment')
        plt.grid()
        plt.show()

    def monitor(self, persistance=None):
        '''
        Shows and overdraws measurments from the spectrum analyzer as it updates

        Keywords:
        persistance = overlays graphs continiously when on (bool) (Default=OFF)
        '''
        xAxis = []
        for i in range(601):
            xAxis.append(i)

        self.fig = plt.figure()

        plt.xlabel('Center Frequency +/- 600 Points')
        plt.ylabel('Amplitude [dB]')
        plt.title('HP8562 SA Measurment')
        plt.grid()

        def animate(i):
            if persistance is None:
                plt.clf()
            self.list = self.getMeasurmentList()
            plt.scatter(xAxis, self.list, s=1)
            self.line = plt.plot(xAxis, self.list)

        self.ani = animation.FuncAnimation(self.fig, animate, interval=10)
        plt.show()
        


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
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
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
        if state:
            self.commandInstrument('OUTPUT:STATE OFF')
        else:
            self.commandInstrument('OUTPUT:STATE ON')

    def setRF(self, frequency, amplitude):
        '''
        Set RF frequency in float MHz and (float) amplitude in dB
        '''
        self.commandInstrument(
            "FREQ " +
            str(frequency) +
            'MHZ' +
            ": " +
            "POW" +
            str(amplitude) +
            'DBM')


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
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
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
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()
        self.instance = self.rm.open_resource(str(self.visaID))
        self.commandInstrument(
            '*RST; *CLS; STATus:PRESet; *SRE 0; *ESE 0; RST; CLR')

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
        # Check if instrument output is disabled and if so keep it disabled
        # unsless user enables it
        if self.queryInstrument('OUT') is 0 and enable is None:
            enable = False
        if enable is False:
            self.commandInstrument('OUT 0')
        else:
            self.commandInstrument('OUT 1')
        # Set channel if instrument has more than one channel
        if channel is None:
            self.commandInstrument('VSET' + str(voltage))
        else:
            self.commandInstrument('VSET' + str(channel) + ',' + str(voltage))
        # Return the current output
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
        # Check if instrument output is disabled and if so keep it disabled
        # unsless user enables it
        if self.queryInstrument('OUT') is 0 and enable is None:
            enable = False
        if enable is False:
            self.commandInstrument('OUT 0')
        else:
            self.commandInstrument('OUT 1')
        # Set channel if instrument has more than one channel
        if channel is None:
            self.commandInstrument('ISET' + str(current))
        else:
            self.commandInstrument('ISET' + str(channel) + ',' + str(current))
        # Return the current output
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

    def setUP(
            self,
            current,
            voltage,
            channel=None,
            enable=None,
            ocp=False,
            ovp=0):
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


class HP3852A(object):
    '''
    HP 3852A Masure Mainframe
    - HP47701A 5 1/2Ditit Voltmeter
    '''

    def __init__(self, bus, addr):
        '''
        Initiate GPIB instance
        '''
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()
        self.instance = self.rm.open_resource(str(self.visaID))
        #self.commandInstrument('*RST; *CLS')

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

    def checkModule(self, module):
        return(queryInstrument())

    '''
    Set Voltage DAC
    Input:
        Module Number: [0 ; 7]
        Channel: [0 ; 1]
        Voltage: [10.23V ; 10.23] [V]
        '''

    def setVDAC(self, module, channel, voltage):
        '''self.commandInstrument("USE " + str(module) + "00")'''
        self.commandInstrument(
            "APPLY DCV " +
            str(module) +
            "0" +
            str(channel) +
            ", " +
            str(voltage))

    '''
    Set ARB DAC Waveform
    Input:
        Module Number: [0 ; 7]
        Channel: [0 ; 1]
        Select Waveform: [0 ; 63]
    '''
    def setWave(self, module, channel, voltage):
        '''
        '''
        
    '''
    Scan Channels via Multiplexer
    Input:
        moduleMeter: Module number of the voltmeter to use [0 ; 7]
        moduleMux: Module number of the multiplexer module to use [0 ; 1]
        delay: Set delay between measurments (more than 0.2s causes an visa error)
    '''
    def muxMeas(self, moduleMeter, moduleMux, delay):
        self.commandInstrument("RST " + str(moduleMeter) + "00")
        self.commandInstrument("USE " + str(moduleMeter) + "00")
        self.commandInstrument("CONF DVC")
        self.commandInstrument("NPLC 0.1")
        self.commandInstrument("DELAY" + str(delay))
        self.commandInstrument("RANGE 5") 
        dataStr = (self.queryInstrument("MEAS DCV, 300-310"))
        dataStr = dataStr[:-2]
        dataStr = dataStr.split("\r\n")
        print(dataStr)
        dataFloat = list(map(float, dataStr))
        print(dataFloat[1])

        
        


class KY236(object):
    '''
    HP 3852A Masure Mainframe
    - HP47701A 5 1/2Ditit Voltmeter
    '''

    def __init__(self, bus, addr):
        '''
        Initiate GPIB instance
        '''
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()
        self.instance = self.rm.open_resource(str(self.visaID))
        
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

        '''
        Set voltage and get current
        Input:
        Voltage input, floating point or scientific, use "."
        '''

    def measureCurrent(self, voltage):
        self.commandInstrument(
            "F0,0 B" +
            str(voltage) +
            ",0,100 N1 R1 S3 G4,2,0 X")
        return(float(self.queryInstrument("H0X")))
        
    def LinVoltageSweep(self, startVoltage, stopVoltage, numberOfMeasurments):
        '''
        Input:
            start voltage (float)
            stop voltage (float)
            number of measurments (int)
        returns:
            list of measurments
        '''
        self.commandInstrument("F0,0 N1 R1 S3 G4,2,0 X")
        measurments = []
        voltageStep = (stopVoltage - startVoltage) / numberOfMeasurments
        voltage0 = startVoltage
        for i in range(0, numberOfMeasurments):
            voltage0 = voltage0 + voltageStep
            self.commandInstrument("B" + str(voltage0) + ",0,200 X")
            measurments.append(float(self.queryInstrument("H0X")))
        return measurments
    
    def LogVoltageSweep(self, startVoltage, stopVoltage, numberOfMeasurments):
        '''
        Input:
            start voltage (float)
            stop voltage (float)
            number of measurments (int)
        returns:
            list of measurments
        '''
        self.commandInstrument("F0,0 N1 R1 S3 G4,2,0 X")
        measurments = []
        voltage0 = startVoltage
        for i in range(0, numberOfMeasurments):
            voltage0 = pow(10, (math.log10(stopVoltage - startVoltage) / numberOfMeasurments * i)) + startVoltage
            self.commandInstrument("B" + str(voltage0) + ",0,200 X")
            measurments.append(float(self.queryInstrument("H0X")))
        return measurments
    
    
    def plotVI(self, startVoltage, stopVoltage, numberOfMeasurments, sweepType='Lin'):
        '''
        Input:
            start voltage (float)
            stop voltage (float)
            number of measurments (int)
            sweep Type:
                DEFAULT: Lin Linear
                OPTION: Log Logarithmic
            
        plots:
            VI Curve
        '''
        measurments = []
        testVoltages = []
        
        if sweepType is 'Lin':
            voltage0 = startVoltage
            voltageStep = (stopVoltage - startVoltage) / numberOfMeasurments
            for i in range(0, numberOfMeasurments):
                voltage0 = voltage0 + voltageStep
                testVoltages.append(voltage0)
            measurments = self.LinVoltageSweep(startVoltage, stopVoltage, numberOfMeasurments)
            
        if sweepType is 'Log':
            voltage0 = startVoltage
            for i in range(0, numberOfMeasurments):
                voltage0 = pow(10, (math.log10(stopVoltage - startVoltage) / numberOfMeasurments * i)) + startVoltage
                testVoltages.append(voltage0)
            measurments = self.LogVoltageSweep(startVoltage, stopVoltage, numberOfMeasurments)
        
        
        plt.ylabel('Curent [A]')
        plt.xlabel('Voltage [V]')
        plt.plot(testVoltages,measurments)
        plt.plot(testVoltages,measurments)
        plt.show()

        
class HP3577(object):
    '''
    classdocs
    This class provides an easy interface to the HP3577(A) 5Hz-200MHz Network Impeadance Meter / VNA
    '''
    def __init__(self, bus, addr):
        '''
        Initiate GPIB instance
        '''
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()
        self.instance = self.rm.open_resource(str(self.visaID))
     
        
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

        '''
        Set voltage and get current
        Input:
        Voltage input, floating point or scientific, use "."
        '''       
        
    def getStatusByte(self):
        '''
        Read the status Byte of the instrument
        '''
        return(self.instance.read_stb())
        
        
    def sweepComplete(self):
        '''
        Tests if the measurments have been completed
        '''
        byte = self.getStatusByte()
        mask = 1 << 2 #Bit B2 is the measurment complete status byte
        if(byte & mask == 4):
            return(True)
        else:
            return(False)
        
        
    def getData(self, channel):       
        '''
        Intup Measurment channe: 'R', 'A', 'B'
        Return: numpy array
        
        Warning: Does not set number of meas. points
        '''
       
        self.commandInstrument('FM2') #Turn characters off, turn buss diagnostics off, set data type to binary     
        binary = self.instance.query_binary_values('DR' + str(channel), datatype='d', is_big_endian=True) #Read binary data (faster)
        
        nos = int(len(binary)/2)
        registerDataListComplex = []
        
        sample = 0
        for i in range(0, nos):
            komplex = complex(float(binary[sample]), float(binary[sample+1]))
            registerDataListComplex.append(komplex)
            sample = sample + 2;    
        
        self.commandInstrument('CH1, FM1, BD1') #Turns all back on
        return(registerDataListComplex)
        
        
    def getDataNP(self, channel):
        '''
        Intup Measurment channe: 'R', 'A', 'B'
        Return: numpy array
        
        Warning: Does not set number of meas. points
        '''
        return(np.asarray(self.getData(channel)))
        
        
    def plotPolar(self, channel):
        '''
        Returns a polar plot of the selected channel
        '''
        X = []
        Y = []
        
        data = self.getData(channel)
        
        nos = len(data)
        
        for i in range(0, nos):
            X.append(data[i].real)
            Y.append(data[i].imag)

        plt.scatter(X,Y, color='red')
        plt.show()
      
        
    def getMag(self, dataListComplex):
        magnitudeList = []
        for i in range(0, len(dataListComplex)):
            magnitudeList.append(math.sqrt(pow(dataListComplex[i].real, 2) + pow(dataListComplex[i].imag, 2)))
        return(magnitudeList)
        
        
    def getPhase(self, data):
        phaseList = []
        for i in range(0, len(data)):
            phaseList.append()
        return(phaseList)
        
        
    def setAVERAGE(self, averageMode):  
        '''
        Number of samples which get averaged
        Possible Settings:
            0 = OFF
            1 = 4
            2 = 8
            n = 2^(n+1)
            7 = 256
        '''
        self.commandInstrument('AB'+str(averageMode))
  
    
    def plotMag(self, channel):
        '''
        Will plot the linear response of selected channel in [mV]
        '''
        plt.plot(self.getMag(self.getData(channel)))

        
    def plotPhase(self, channel):
        plt.plot(self.getPhase(self.getData(channel)))
        
        
    def plotMagdBm(self, channel, sourceResistance=50):
        '''
        Will plot log magnitude of channel in [dBm] assuming 50Ohm system
        '''
        magnitudeList = self.getMag(self.getData(channel))
        magnitudeListLog = []
        
        nos = len(magnitudeList)
        for i in range(0, nos):
            magnitudeListLog.append(10 * math.log10(pow(magnitudeList[i], 2) / sourceResistance))
            
        plt.plot(magnitudeListLog)
      

    def setATTEN(self, channel, attenuation, impeadance):
        return()
    
        
    def setRBW(self, rbw): ##1, 10, 100, 1000 
        '''
        #rb sets ResolutionBandWitdh for all channels, valid inputs for rb: 1, 10, 100, 1000 [HZ]
        #SWEEP time has to be set in relation to RBW - see manual page [TODO]
        '''
        return()

    
    def setSweep(self, sweepTime, sweepMode='continious', sweepType='linear'):
        mode = 1
        typ = 1
        
        if(sweepMode == 'continious'):
            mode = 1
        elif(sweepMode == 'single'):
            mode = 2       
        elif(sweepMode == 'manual'):
            mode = 3
        else:
            print("ERROR SWEEP MODE ARGUMENT INVALID")
            return()

        if(sweepType == 'linear'):
            typ = 1     
        elif(sweepType == 'alternate'):
            typ = 2 
        elif(sweepType == 'log'):
            typ = 3             
        elif(sweepType == 'cwr'):
            typ = 5 
        else:
            print("ERROR SWEEP TYPE ARGUMENT INVALID")
            return()
            
        print('ST'+str(typ)+', SM' + str(mode) + ', SWT ' + str(sweepTime) + ' MSC')
        self.commandInstrument('ST'+str(typ)+', SM' + str(mode)+ ', SWT ' + str(sweepTime) + ' MSC')
        return()
        
        
    def trigger(self):
        '''
        Will imeadiatly trigger insturment
        '''
        self.commandInstrument('TG4')
        
    
    def setFRQ(self, startF, stopF):
        '''
        Set start and stop frequency in MHZ
        '''
        self.commandInstrument('FRA ' + str(startF) + ' MHZ, FRB ' + str(stopF) + 'MHZ')
        
        
    def setCenterFRQ(self, centerF):
        '''
        set center freqeuency in MHz
        '''
        self.commandInstrument('FRC '+str(centerF)+'MHZ')        
      
        
    def normalize(self, channel):
        self.commandInstrument('NRM')
        
        
    def normalizeShort(self, channel):
        self.commandInstrument('NRS')
       
        
    def setAVERAGE(self, averageMode):
        return()
        
        
    def bodePlot(self, data):
        return()
        
        
    def saveSettings(self, memorySlot):
        '''
        Saves current settings to memory slot 1-5
        '''
        if( 5 > memorySlot < 1):
            return("ERROR MEMORY SLOT OUT OF RANGE")
        self.commandInstrument('SV'+str(memorySlot))
        return()
                
        
    def restoreSettings(self, memorySlot):
        '''
        Gets settings to memory slot 1-5
        '''
        if( 5 > memorySlot < 1):
            return("ERROR MEMORY SLOT OUT OF RANGE")
        self.commandInstrument('RC'+str(memorySlot))
        return()
        
        
    def reset(self):
        self.commandInstrument('RST')
        
        
    def getSinglePoint(self, channel, frequency, sampleTime=0.05):
        '''
        Get a single mesurement from a single channel / frequency [MHz] via CW, sample time is in [ms]
        TODO Does not fully work yet ... Dont receive data ???
        '''

        self.commandInstrument('ST5')
        self.commandInstrument('SFR ' + str(frequency) + ' MHZ')
        self.commandInstrument('MSR ' + str(sampleTime) + ' MSC')
        time.sleep(1)
        self.commandInstrument('TRG')
        time.sleep(1)
        return(self.instance.query_binary_values('DR' + str(channel), datatype='d', is_big_endian=True)) #Read binary data (faster)
        
        
    def put1Network(self, channel, startF, stopF):
        self.setFRQ(startF, stopF)
        while(self.sweepComplete == False):
            x=1
        buffer = self.getData(channel)

        fObject = Frequency(startF, stopF, len(buffer), 'mhz')
        Net = Network(frequency=fObject, s=buffer, z0=[50], name=str(channel))
        
        return Net

        

        

        

        
    

        


 
        
            
            
        
