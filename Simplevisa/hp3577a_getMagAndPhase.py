# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 19:05:52 2019

@author: justRandom
"""

import simplevisa
import matplotlib.pyplot as plt
import numpy as np



hp = simplevisa.HP3577(0, 11)
hp.setFrequency(100, 10e7)
mag, phase, f = hp.bodePlot('R', mode='log')


print('Maximum magnitude: %d [dBm] at: %d [Hz]' %(np.amax(mag), f[np.argmax(mag)]))
print('Minimum magnitude: %d [dBm] at: %d [Hz]' %(np.amin(mag), f[np.argmin(mag)]))