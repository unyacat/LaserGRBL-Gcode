# -*- coding: utf-8 -*-
'''
G code generater to laser cutting adjustment

Copyright (c) 2020 DenshiKousakuSenka
 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php

This script create squares with varying feed rate and pass.
If the output file already exists, it will be overwritten.
Be sure to focus the laser on the material surface before start operation.
This script made for NEJE Master 2
'''

# parameters
fname = 'LaserEngraveAdjust3'
F0 = 500    # initial feed rate mm/min
dF = 100    # pitch of changing feed rate
M = 6       # number of feed rates
S0 = 500    # initial laser power
dS = 100    # pitch of changing laser power
smax = 1000 # max lase power
N = 5           # number of lser powers
p = 3           # square pitch
L = 2       # square size

# Codes
L2 = L * 0.5
with open(fname+'.nc', mode='w') as fout:
    # Initialize
    fout.write('$32=1\n')       # Enable laser mode
    fout.write('F500;\n')           # Feed rate
    fout.write('G49 G80;\n')    # G49:Cancel tool offset, G80: Motion mode cancel
    fout.write('G17 G21;\n')    # G17: Select XY plane, G21: units mm
    fout.write('G90;\n')        # G90: Absolute distance mode
    fout.write('M05 S0;\n')     # M05: Stop laser, S0: pwm=0
    # Write rectangle
    for f in range(M + 1):
        cx = (f + 0.5) * p
        for s in range(N + 1):
            cy = (s + 0.5) * p
            ss = S0 + s * dS
            if ss > smax:
                ss = smax
            fout.write('M04 S{0:d};\n'.format(ss))
            fout.write('F{0:d};\n'.format(F0 + f * dF))
            fout.write('G00 X{0:.3f} Y{1:.3f};\n'.format(cx - L2, cy - L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx - L2, cy + L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx + L2, cy + L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx + L2, cy - L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx - L2, cy - L2))
            fout.write('M05;\n')        # laser off
            fout.write('\n')
    # Finalize
    fout.write('S0;\n')
    fout.write('G00 X0.Y0.Z0.;\n')      # go back to zero
    fout.write('$32 = 0\n')     # Disable laser mode
    fout.write('M30;\n')        #program end
