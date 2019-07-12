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


class dualSmu(object):
    def __init__(self, SMU0, SMU1):
    '''
    Initiate GPIB instance
    '''
    self.smu0 = SMU0
    self.smu1 = SMU1

    '''
    Provides a wrapper for dual Source Measurment Unit measurments 
    smu0, smu1: SMU Object
    '''
    def outputCharacteristicCurve(self, IBEstart, IBEstop, IBEstep, VmaxBE, VCEstart, VCEstop, VCEstep, ImaxCE, plot=False, save=False, fileName="curveTrace.pdf"):
        '''
        Will do a transistor Vce to Ice measurment dependend on VBe
        
        SMU0 should be connected to the base, SMU1 to the collector
        LO for SMU0/1 goes to the collector
        
        IBEstart : [V][float] 
            VBE Curve start voltage (normally 0)
        IBEstop : [V][float]  
            VBE stop voltage
        IBEbstep : [V][float] 
            VBE step in volts between traces            
        VmaxBE : [A][float] 
            Maximal allowable base current which is sourced
        VCEstart : [V][float] 
            Start Voltage for trace
        VCEstop : [V][float] 
            Stop Voltage for trace
        VCEstep : [V][float]
            VCE step in volts between traces 
        ImaxCE : [A][float] 
            Maximal allowable collector current which is sourced
        plot : bool
            Optional, will generate a nicely labeled plot
            
        return: array[VBE_Step_Bin][ICE_Measurments]
            Will return a two dimensional float array. One dimension holds
            measurments for each VBE trace
            The inner dimension will hold the start-stop sweep measurments
            for ICE [float][A]
        '''
        numberOfTraces = (IBEstop - IBEstart) / IBEbstep
        numberOfMeasurments = (VCEstop - VCEstart) / VCEstep
        outArr[numberOfTraces][numberOfMeasurments] = 0
        self.smu0.integrationTime(3)
        self.smu1.integrationTime(3)
        for traceIter in range(0, numberOfTraces):
            self.smu0.setCurrent((IBEstart + traceIter * IBEbstep), ImaxBE)
            outArr[traceIter] = self.smu1.linearVoltageSweep(VCEstart, VCEsop, VCEstep, delay=0, complianceCurrent=ImaxCE)
        #Plot the optained array
        if plot is True:
            plt.cla()
            for traceIter in range(0, numberOfTraces):
                plt.plot(outArr[traceIter]) 
            plt.show
        if plot is true and save is true:
            plt.savefig(fileNam)
        return outArr


class Keithley23x(object):
    '''
    Provides simple interface to Keithley 23x series SMU's
    '''
    def __init__(self, bus, addr):
        '''
        Initiate GPIB instance
        '''
        self.visaID = 'GPIB' + str(bus) + '::' + str(addr) + '::INSTR'
        self.rm = visa.ResourceManager()
        self.instance = self.rm.open_resource(str(self.visaID))
        del self.instance.timeout #DISABLE GPIB TIMEOUT FOR THIS DEVICES!!!
        
         voltage, complianceLevel, delay=0, sourceRange=0, complianceRange=0
        
    def currentSource(self, current, complianceLevel, delay=0, sourceRange=0, compliancRange=0):
        '''
        Get single current measurment via a constant voltage measurment Will set up the instrument.
        
        voltage 
            Voltage as [V] float
              
        complianceLevel [float][V]
            Set the maximum voltage output of the current source
            
        delay [int][ms]
            Delay between measurments
      
        sourceRange
            Output Range for the current source
            0 = Auto
            1 = lnA
            2 = lOnA
            3 = lOOnA
            4 = lJ.IA
            5 = lOJ.IA
            6 = lOOJ.IA
            7 = lmA
            8 = lOrnA
            9 = lOOmA
            10 = lA (238 only)
            
        complianceRange [int]
        Output Range for the current source (limiter)
            0 = Auto
            1 = 1.1V (236, 237) 1.5V (238)
            2 = 11V (236, 237) 15V (238)
            3 = 110V
            4 = 1100V (237, HV mode has to be activated)
        
        return [float]
            Returns the measured current as float [A]
        '''
        self.outputDataFormat()
        self.sourceAndFunction(1, False) #Set Current source function, single 
        self.biasOperation(voltage, setRange, 200)
        self.compliance(compliance, 0)
        self.triggerControl(0)
        self.triggerConfiguration()
        self.startOp()
        measurment = float(self.triggerAndMeasure())
        self.stopOp()
        return measurment 

    def voltageSource(self, voltage, complianceLevel, delay=0, sourceRange=0, complianceRange=0):
        '''
        Get single current measurment via a constant voltage measurment Will set up the instrument.
        
        voltage 
            Voltage as [V] float
              
        sourceRange
            Output voltage range for the current source (limit)
            0 = Auto
            1 = 1.1V (236, 237) 1.5V (238)
            2 = 11V (236, 237) 15V (238)
            3 = 110V
            4 = 1100V (237, HV mode has to be activated)
            
        complianceLevel
            Set the maximum output current of the voltage source [float][A]
        
        complianceRange     
            Sets the range of the compliance limiter
            0 = Auto
            1 = lnA
            2 = lOnA
            3 = lOOnA
            4 = lJ.IA
            5 = lOJ.IA
            6 = lOOJ.IA
            7 = lmA
            8 = lOrnA
            9 = lOOmA
            10 = lA (238 only)
            
        delay
            Set the delay between measurments [ms]

        float
            Returns the measured current as float [A]
        '''
        self.outputDataFormat()
        self.sourceAndFunction(0, False)
        self.biasOperation(voltage, sourceRange, delay)
        self.compliance(complianceLevel, complianceRange)
        self.triggerControl(0)
        self.triggerConfiguration()
        self.startOp()
        measurment = float(self.triggerAndMeasure())
        self.stopOp()
        return measurment   
    
    
    def linearVoltageSweep(self, start, stop, step, delay=0, complianceCurrent=0.1):
        '''
        Will return a list of all a linear sweep measurment
        
        start:
            Start point [float][V]
        stop:
            Stop point [float][V]
        step:
            Stop point [float][V]
        delay:
            Delay between measurments
        complianceCurrent:
            Max Current [float][A] put out by the current source   
        '''
        self.outputDataFormat(lines=2)
        self.sourceAndFunction(0, True) #Constant Voltage / Sweep mode
        self.compliance(complianceCurrent, 0) 
        self.triggerControl(True) 
        self.triggerConfiguration() #Default Trig Config
        self.createSweepListLinearStair(0, delay, step, start, stop)
        self.startOp()
        raw = self.triggerAndMeasure() #Get the list
        self.stopOp()
        meas = map(float, raw.split(","))
        return(meas)
        
    def linearCurrentSweep(self, start, stop, step, delay=0, complianceVoltage=10):
        '''
        Will return a list of all a linear sweep measurment
        
        start:
            Start point [float][V]
        stop:
            Stop point [float][V]
        step:
            Stop point [float][V]
        delay:
            Delay between measurments
        complianceCurrent:
            Max Current [float][A] put out by the current source   
        '''
        self.outputDataFormat(lines=2)
        self.sourceAndFunction(1, True) #Constant Voltage / Sweep mode
        self.compliance(complianceVoltage, 0) 
        self.triggerControl(True) 
        self.triggerConfiguration() #Default Trig Config
        self.createSweepListLinearStair(0, delay, step, start, stop)
        self.startOp()
        raw = self.triggerAndMeasure() #Get the list
        self.stopOp()
        meas = map(float, raw.split(","))
        return(meas)
        

    def stopOp(self):
        '''
        Stops the SMU output
        '''
        self.setOpState(False)
        
    def startOp(self):
        '''
        Starts the SMU output
        '''
        self.setOpState(True)
 
    #----------------------------------------------------------------------------------------
    #GPIB LOW LEVEL FUNCTIONS  
    def commandInstrument(self, command):
        '''
        Send a GPIB command to instrument
        Raises an exception if device unreachable
        '''
        code = self.instance.write(str(command))
        if '<StatusCode.success: 0>' not in str(code):
            raise Exception("Keithley 23x did not response!")

    def queryInstrument(self, request):
        '''
        Query GPIB Device
        '''
        return(self.instance.query(request))
        
    def createSweepListFixedLevel(self, level, Range, delay, count):
        '''
        Creates a fixed Level sweep list (values stay the same for number of measurments)
        level:
            Specifies output level of sweep source (I or V):             
        rang:
            range - Selects the source range:
                0= Auto
                1= lnA
                2= lOnA
                3= lOOnA
                4 = lJ.IA
                5 = lOJ.IA
                6 = lOOJ.IA
                7= lmA
                8= lOrnA
                9= lOOmA
                10 = lA ('238)
    
                V-source
                Auto
                1.1V ('236, 237); 1.5V (238)
                11 V (236, 237); 15V ('238)      
        delay:
            Sweep delay in milliseconds (0-65000)           
        count:
            Number of measurments
        '''
        self.commandInstrument("Q0," +str(level) + "," + str(Range) + "," + str(delay) + "," + str(count)+" X")
        return
    
    def createSweepListLinearStair(self, Range, delay, step, start, stop):
        '''
        Creates a linear staircase sweep list            
        rang:
            range - Selects the source range:
                0= Auto
                1= lnA
                2= lOnA
                3= lOOnA
                4 = lJ.IA
                5 = lOJ.IA
                6 = lOOJ.IA
                7= lmA
                8= lOrnA
                9= lOOmA
                10 = lA ('238)
    
                V-source
                Auto
                1.1V ('236, 237); 1.5V (238)
                11 V (236, 237); 15V ('238)      
        delay:
            Sweep delay in milliseconds (0-65000)           
        step:
            Step between measurments 
        start:
            Start Value
        stop:
            Stop value      
        '''
        self.commandInstrument("Q1," + str(start) + "," + str(stop) + "," + str(step) + "," + str(Range) + "," + str(delay) + "X")
        return
    
    def createSweepListLogStair(self, Range, delay, points, start, stop):
        '''
        Creates a linear staircase sweep list            
        rang:
            range - Selects the source range:
                0= Auto
                1= lnA
                2= lOnA
                3= lOOnA
                4 = lJ.IA
                5 = lOJ.IA
                6 = lOOJ.IA
                7= lmA
                8= lOrnA
                9= lOOmA
                10 = lA ('238)
    
                V-source
                Auto
                1.1V ('236, 237); 1.5V (238)
                11 V (236, 237); 15V ('238)      
        delay:
            Sweep delay in milliseconds (0-65000)           
        points:
            Number of Measurments 
        start:
            Start Value
        stop:
            Stop value      
        '''
        self.commandInstrument("Q2," + str(start) + "," + str(stop) + "," + str(points) + "," + str(Range) + "," + str(delay) + "X")
        return
    
        
    def setOpState(self, state):
        if state is True:
            setState = 1       
        else:
            setState = 0
        self.commandInstrument("N"+str(setState)+"X")
    
    def modifySweepList(self, level, rang, delay, first, last):
        '''
        Description:
            To change the source level, source range, or sweep 
            delay of any points in a sweep list
            of a previously created or appended waveform       
        level:
            Specifies output level of sweep source (I or V):             
        rang:
            range - Selects the source range:
                0= Auto
                1= lnA
                2= lOnA
                3= lOOnA
                4 = lJ.IA
                5 = lOJ.IA
                6 = lOOJ.IA
                7= lmA
                8= lOrnA
                9= lOOmA
                10 = lA ('238)
    
                V-source
                Auto
                1.1V ('236, 237); 1.5V (238)
                11 V (236, 237); 15V ('238)      
        delay:
            Sweep delay in milliseconds (0-65000)           
        first:
            First data point (1-1000)        
        last:
            Last data point (1-1000)
        '''
        self.commandInstrument("A" +str(level) + "," + str(rang) + "," + str(delay) + "," + str(first) + "," + str(last)+" X")
        return
    
    
    def biasOperation(self, level, rang, delay):
        '''
        Description:
            To program the de bias operation, the non-triggered sweep source value, and the toFF
            source value of pulsed sweeps.
            
        level:
            Specifies output level of sweep source in V or A
            
        rang:
            range - Selects the source range:
                0= Auto
                1= lnA
                2= lOnA
                3= lOOnA
                4 = lJ.IA
                5 = lOJ.IA
                6 = lOOJ.IA
                7= lmA
                8= lOrnA
                9= lOOmA
                10 = lA ('238)
    
                V-source
                Auto
                1.1V ('236, 237); 1.5V (238)
                11 V (236, 237); 15V ('238)      
        delay:
            Sweep delay in milliseconds (0-65000) 
        '''
        self.commandInstrument("B" + str(level) + "," + str(rang) + "," + str(delay) + " X")
        return
    
    def sourceAndFunction(self, mode, sweep=False):
        '''
        Description:
            To program a source (V or I) and a function (de or sweep).
            
        mode:
            0  : Source Voltage measure Current
            1  : Source Current measure Voltage
            
        sweep:
            DC if False
            Sweep if True     
        '''
        Sweep = 0
        if sweep is True:
            Sweep = 1
               
        self.commandInstrument("F" + str(mode) + "," + str(Sweep) + "X")
        return
    
    def outputDataFormat(self, items=4, form=2, lines=0):
        '''
        Description:
            To select the type, format, and quantity of output data transmitted over the bus.
        items:
            O = Noitems
            1 = Source value
            2 = Delay value
            4 = Measure value
            8 = Time value        
        format:
            0 = ASCll data with prefix and suffix
            1 = ASCll data with prefix, no suffix
            2 = ASCll data, no prefix or suffix
            3 = HP binary data
            4 = IBM binary data       
        lines:
            0 = One line of de data per talk
            1 = One line of sweep data per talk
            2 = All lines of sweep data per talk
        '''
        self.commandInstrument("G" + str(items) + "," + str(form) + "," + str(lines) + " X")
        return
    
    
    def triggerAndMeasure(self):
        '''
        To provide an immediate trigger stimulus from the IEEE-488 bus.
        '''
        return(self.queryInstrument("H0X"))
        
    
    
    def selfTests(self, test):
        '''
        To restore factory defaults and test memory and front panel display.
        test:
            0 = Restore factory defaults
            1 = Perform memory test
            2 = Perform display test
        '''
        self.commandInstrument("J" + str(test) + "X")
        time.sleep(4)
        return
    
    def compliance(self, level, rang):
        '''
        To program the compliance value and compliance/measurement range.
        
        The L command sets the compliance level for the programmed source and selects the
        measurement range. If the unit is programmed to source current, then the L command
        sets a voltage compliance and selects a voltage measurement range. Conversely,
        if the unit is programmed to source voltage, the L command sets a current
        compliance and seleCts a current measurement range.
        
        level:
            Specifies the compliance level (I or V):        
        rang:
                range - Selects the source range:
                0= Auto
                1= lnA
                2= lOnA
                3= lOOnA
                4 = lJ.IA
                5 = lOJ.IA
                6 = lOOJ.IA
                7= lmA
                8= lOrnA
                9= lOOmA
                10 = lA ('238)
    
                V-source
                Auto
                1.1V ('236, 237); 1.5V (238)
                11 V (236, 237); 15V ('238)  
        '''
        self.commandInstrument("L" + str(level) + "," + str(rang) + " X")
        return
    
    def operate(self, operate):
        '''
        To place the instrument in operate or standby mode.
        
        operate:
            True = Output On
            False = Output Off
        '''
        Out = 1
        if operate is False:
            Out = 0
        self.commandInstrument("N" + str(Out) + " X")
        return
    
    def outputSense(self, local):
        '''
        To select local or remote output sensing.
        
        local:
            True = Local
            False = Remote
        '''
        Out = 1
        if local is False:
            Out = 0
        self.commandInstrument("O" + str(Out) + " X")
        return
    
    def filter(self, mode):
        '''
        To control the number of readings averaged.
        
        mode:
            0 = Filter disabled
            1 = 2readings
            2 = 4readings
            3 = 8readings
            4 = 16readings
            5 = 32readings
        '''
        self.commandInstrument("P" + str(mode) + " X")
        return
    
    #TODO hole range of sweep lists....
    #TODO hole range of sweep lists....
    #TODO hole range of sweep lists....
    #TODO hole range of sweep lists....
    
    def triggerControl(self, triggerOn):
        '''
        To enable/ disable input and output triggers.
        
        triggerOn:
            True = Enable input triggering and generation of output triggers
            False = Disable input triggering and generation of output triggers
        '''
        Out = 1
        if triggerOn is False:
            Out = 0
        self.commandInstrument("R" + str(Out) + " X")
        return
    
    def integrationTime(self, mode):
        '''
        To control the integration time and resolution.
        mode:
            0 = 416us      Fast                    4-digit
            1 = 4ms        Medium                  5-digit
            2 = 16.67ms    Line Cycle (60Hz)       5-digit
            3 = 20ms       Line Cycle (50Hz)       5-digit
        '''
        self.commandInstrument("S" + str(mode) + " X")
        return
    
    def triggerConfiguration(self, orgin=4, triggerIn=0, triggerOut=0, triggerEnd=0):
        '''
        To specify the origin and effect of an input trigger, and when output triggers are generated.
        orgin:
            Specifies the origin of input triggers:
            O = IEEEX
            1 = IEEE GET
            2 = 1EEETalk
            3 = External (TRIGGER IN pulse)
            4 = Immediate only (front panel MANUAL key or HOX command)         
        triggerIn:
            Specifies the effect of an input trigger:
            0 = Continuous (no trigger needed to continue S-D-M cycles)
            1 = SRC DLY MSR (trigger starts source phase)
            2 = SRC,.DLY MSR (trigger starts delay phase)
            3 = SRC,.DLY MSR
            4 = SRC DL Y "MSR (trigger starts measure phase)
            5 = SRC DLY MSR
            6 = SRC OLY MSR
            7 = SRC DLY MSR
            8 = Single pulse       
        triggerOut:
            Specifies when an output trigger is generated:
            0 = None during sweep
            1 = SRC DLY MSR (end of source phase)
            2 = SRC DLY,.MSR (end of delay phase)
            3 = SRC DLY,.MSR
            4 = SRC DLY MSR" (end of measure phase)
            5 = SRC DLY MSR"
            6 = SRC DLY MS"
            7 = SRC DLY MSR
            8 = Pulse end"   
        triggerEnd:
            Sweep End trigger out:
            0 = Disabled
            1 = Enabled    
        '''
        self.commandInstrument("T" + str(orgin) + "," + str(triggerIn) + "," + str(triggerOut) + "," + str(triggerEnd) + " X")
        return
    
    def getStatus(self, status):
        '''
        To obtain instrument status and configuration.
        
        0  Send model number and firmware revision
        1  Send error status word
        2  Send stored ASCll string ( "02" command string)
        3  Send machine status word
        4  Send measurement parameters
        5  Send compliance value
        6  Send suppression value
        7  Send calibration status word
        8  Send defined sweep size
        9  Send warning status word
        10 Send first sweep point in compliance
        11 Send sweep measure size
        '''
        return(self.queryInstrument("B" + str(status) + " X"))

    
    def hvRange(self, hvRangeEnabled=False):
        '''
        To control the output of voltages on the llOOV range of a Model237 Source Measure
        Unit.
        '''
        Out = 0
        if hvRangeEnabled is True:
            Out = 1
        self.commandInstrument("V" + str(Out) + " X")
        return
    
    def defaultDelay(self, delayEnabled=True):
        '''
        To enable/ disable the default delay of the source-delay-measure cycle.
        '''
        Out = 0
        if delayEnabled is True:
            Out = 1
        self.commandInstrument("W" + str(Out) + " X")
        return
    
    def surpress(self, enable=False):
        '''
        To enable/ disable the suppression of subsequent readings with the present measurement.
        '''
        Out = 0
        if enable is True:
            Out = 1
        self.commandInstrument("Z" + str(Out) + " X")
        return

        
    
    
    
    
    
    
    
    
    
        

        
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
        
        self.commandInstrument('FM1') #Turns all back on
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
      

    def setAttenuation(self, channel, attenuation='20dB'):
        '''
        Set attenuation of channel, 0dB or 20dB
        '''
        if(attenuation == '0dB'):
            mode = 1
        elif(attenuation == '20dB'):
            mode = 2       
        else:
            print("ERROR ATTEN ARGUMENT INVALID")
            return()  
        self.commandInstrument('A' + str(channel) + str(mode))
        
        
    def setImpeadance(self, channel, impeadance='50Ohm'):
        '''
        Set attenuation of channel, 0dB or 20dB
        '''
        mode = 1
        if(impeadance == '50Ohm'):
            mode = 1
        elif(impeadance == '1MOhm'):
            mode = 2       
        else:
            print("ERROR ATTEN ARGUMENT INVALID")
            return()  
        self.commandInstrument('I' + str(channel) + str(mode))
    
        
    def setRBW(self, rbw='1000HZ'): 
        '''
        #rb sets ResolutionBandWitdh for all channels, valid inputs for rb: 1, 10, 100, 1000 [HZ]
        #SWEEP time has to be set in relation to RBW - see manual page [TODO]
        '''
        mode = 1
        
        if(rbw == '1HZ'):
            mode = 1
        elif(rbw == '10HZ'):
            mode = 2       
        elif(rbw == '100HZ'):
            mode = 3
        elif(rbw == '1000HZ'):
            mode = 4
        else:
            print("ERROR RBW ARGUMENT INVALID")
            return()  
        self.commandInstrument('BW' + str(mode))

    
    def setSweep(self, sweepMode='continious'):
        mode = 1
        
        if(sweepMode == 'continious'):
            mode = 1
        elif(sweepMode == 'single'):
            mode = 2       
        elif(sweepMode == 'manual'):
            mode = 3
        else:
            print("ERROR SWEEP MODE ARGUMENT INVALID")
            return()  
        print('SM' + str(mode))
        self.commandInstrument('SM ' + str(mode))
        return()
        
        
    def setSweepType(self, sweepType='linear'):  
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
        self.commandInstrument('ST'+str(typ))
               
        
    def setSweepTime(self, sweepTime): 
        '''
        Set Sweep time in milliseconds
        '''
        self.commandInstrument('SWT ' + str(sweepTime) + ' MSC') 
    
    
    def doSingleSweep(self):
        '''
        Will set and trigger a single sweep of the instrument
        '''
        self.setSweep(sweepMode='single')
        self.trigger()
        time.sleep(2)
        while(self.sweepComplete() == False):
            time.sleep(3)

 
    def trigger(self):
        '''
        Will imeadiatly trigger insturment
        '''
        self.commandInstrument('TRG')
        
    
    def setFRQ(self, startF, stopF):
        '''
        Set start and stop frequency in MHZ
        '''
        self.commandInstrument('FRA ' + str(startF) + 'MHZ, FRB ' + str(stopF) + 'MHZ')
        
        
    def setCenterFRQ(self, centerF):
        '''
        set center freqeuency in MHz
        '''
        self.commandInstrument('FRC '+str(centerF)+' MHZ')        
      
        
    def normalize(self, channel):
        self.commandInstrument('NRM')
        
        
    def normalizeShort(self, channel):
        self.commandInstrument('NRS')
       
        
    def setAverage(self, averageMode):
        '''
        Set average of measurments
        TODO
        '''
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
    
    def setSourceAmplitude(self, amplitude):
        self.commandInstrument('SAM'+str(amplitude))

        

        

        

        
    

        


 
        
            
            
        
