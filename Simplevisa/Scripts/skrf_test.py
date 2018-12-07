# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 14:55:26 2018

@author: justRandom
"""
import time
import numpy as np
from skrf import Network
import visa

a = [];
for i in range(0, 4):
    real = i /10
    imag = i /100
    a.append(complex(real, imag))

#SKRF smith chart plotting
myNet = Network(f=[0,1,2,3], s=a, z0=[50])
myNet.plot_s_smith()