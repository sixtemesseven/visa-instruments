#!/usr/bin/env python

import simplevisa

if __name__ == '__main__':
    smu = simplevisa.KY236(0,16)
    smu.plotVI(-1,0,100)

