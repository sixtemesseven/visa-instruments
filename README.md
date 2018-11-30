# simplevisa
Simple to use interface for different measurment devices using pyvisa and NI-VISA over GPIB, USB etc.


## (Partially) Supported instruments
* HP856x Series Spectrum Analyzer 
	* Agilent 8562EC
	* Get data over GPIB
	* Continiously plot new data 
	
* HP663xA Series System Power Supplies 
	* HP6632A
	* HP6622A
	* Current and Voltage Settings
	
* HP3775 5Hz-200MHz Network Analyzer
	* Getting Data over GPIB
	* Basic measurment settings
	* Polar plot channel
	
* Rohde & Schwarz SMTxx Series Signal Generators
	* SMT03
	* SMIQ03
	* Basic settings via GPIB
	
* HP / Agilent Switch Module
	* HP3488 
	* Basic functionality for I/O and relays
	
* Rigol Multimeters (Compatible with Agilent and Fluke Protocol)
	* Rigol DM3068 (USB)
	* Basic setup
	* Get measurments over USB
	
* Keithley 23x Series Source Measure Units
	* Setting up measurments
	* Getting data from instrument via GPIB
	* Plotting VI graph

	
## Scripts
### HP662xA Test 
Runs trough CC and CV range while logging and ploting 			
Voltage and Current by the Rigol DM3068 Multimeter.
