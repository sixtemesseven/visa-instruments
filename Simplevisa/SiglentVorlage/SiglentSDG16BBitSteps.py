#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import visa #Uses PyVISA 1.8 and NI-VISA runtime Engine 15.5
import time
import binascii

#USB resource of Device
rm = visa.ResourceManager()
device = rm.open_resource('USB0::0xF4EC::0x1101::SDG6XBAQ1R0071::INSTR')

#Little endian, 16-bit 2's complement
# create a waveform

wave_points = []
for pt in range(0x8000, 0xffff, 1):
    wave_points.append(pt)
wave_points.append(0xffff)
for pt in range(0x0000, 0x7fff, 1):
    wave_points.append(pt)
       
def create_wave_file():
    """create a file"""
    f = open("wave1.bin", "wb")
    for a in wave_points:
        b = hex(a)
        #print 'wave_points: ',a,b
        b = b[2:]
        len_b = len(b)
        if (0 == len_b):
            b = '0000'
        elif (1 == len_b):
            b = '000' + b
        elif (2 == len_b):
            b = '00' + b
        elif (3 == len_b):
             b = '0' + b
        b = b[2:4] + b[:2] #change big-endian to little-endian
        c = binascii.a2b_hex(b) #Hexadecimal integer to ASCii encoded string
        f.write(c)
    f.close()

def send_wave_data(dev):
    """send wave1.bin to the device"""
    f = open("wave1.bin", "rb") #wave1.bin is the waveform to be sent
    data = f.read()
    print ('write bytes:',len(data))
    dev.write_raw("C1:WVDT WVNM,wave1,FREQ,2000.0,TYPE,8,AMPL,4.0,OFST,0.0,PHASE,0.0,WAVEDATA,%s" % (data))
    #"X" series (SDG1000X/SDG2000X/SDG6000X/X-E)
    dev.write("C1:ARWV NAME,wave1")
    f.close()


if __name__ == '__main__':
    """"""

       
    create_wave_file()
    send_wave_data(device)
    device.write("C1:SRATE MODE,TARB,VALUE,333333,INTER,LINE") #Use TrueArb and fixed sample rate to play every point
  
    
