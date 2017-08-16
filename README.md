# visa-instruments
Simple to use interface for different measurment devices using pyvisa and ni-visa over GPIB, USB and ...

Use simplevisa.py by including it in python 3.6+ project or import the content as project into eclipse / pydev.

(Partially) Supported instruments
	- HP856x Series Spectrum Analyzer 
		Tested:
			Agilent 8562EC
	- HP663xA Series System Power Supplies 
		Tested:
			HP6632A
			HP6622A)
	- Rohde & Schwarz SMTxx Series Signal Generators
		Tested:
			SMT03
			SMIQ03
	- HP / Agilent Switch Module
		Tested:
			HP3488 
	- Rigol Multimeter (Compatible with Agilent and Fluke Protocol)
		Tested:
			Rigol DM3068 (USB)


Scripts
	- HP662xA Test 
		Runs trough CC and CV range while logging and ploting 			
		Voltage and Current by the Rigol DM3068 Multimeter.
