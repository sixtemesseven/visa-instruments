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

class GPIB(object):
    '''
    Wraper for basic GPIB / SCPI commands
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

    def setStartF(self, f):
        '''
        set start frequency in MHZ (float)
        '''
        self.commandInstrument("FRA " + str(f) + "MHz")
        
        
    def getData(self, channel):       
        '''
        returns data from measurment register channel in complex format. Number of points depend on number of sampling points
        '''
        
        meas = self.queryInstrument("DR" + str(channel))
        self.dataStr = str(meas)
        registerDataList = self.dataStr.split(",") 
        
        nos = int(len(registerDataList)/2)
        registerDataListComplex = []
        
        sample = 0
        for i in range(0, nos):
            komplex = complex(float(registerDataList[sample]), float(registerDataList[sample+1]))
            registerDataListComplex.append(komplex)
            sample = sample + 2;
        
        return(registerDataListComplex)
        
        
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

        


 
        
            
            
        
