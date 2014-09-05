# test.py
# tests the tablemaker.

from TableMaker import *

ZeroM1 = 'Module_1 p0.0 p0.0 p0.0 p0.0'
GoForwardM1 = 'Module_1 p3.14 p0.0 p0.0 p0.0'
GoForwardM2 = 'Module_2 p3.14 p0.0 p0.0 p0.0'

rS = series([ ZeroM1,
        parallel([ 
            GoForwardM2, GoForwardM1
        ])
     ])
c = CommandBlock()
c.stitch(rS)
print c
