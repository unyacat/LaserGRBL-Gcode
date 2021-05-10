# -*- coding: utf-8 -*-
'''
2021/05/10
正方形を同じところに適度に休憩しながら 2 回連続で描く．

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
fname = 'S600_F800_2times_Sleep-500-2500ms'
F = 800    # 速さ mm/min
S = 600    # 強さ ‰
p = 6      # square pitch
L = 4      # square size
sleep = 0.5  # 休む時間の幅 個数が増えるたびに 0.5, 1, 1.5...
N = 5      # 個数


# Codes
L2 = L * 0.5
with open(fname+'.nc', mode='w') as fout:
    # Initialize
    fout.write('$32=1\n')       # レーザーモードにする
    fout.write('F500;\n')       # 速度 500mm / min
    fout.write('G49 G80;\n')    # G49: Cancel tool offset, G80: Motion mode cancel
    fout.write('G17 G21;\n')    # G17: Select XY plane, G21: units mm
    fout.write('G90;\n')        # G90: Absolute distance mode
    fout.write('M05 S0;\n')     # M05: Stop laser, S0: pwm=0
    # Write rectangle

    for i in range(1, N + 1):
        cx = 5
        cy = (i + 0.5) * p
        for j in range(2):
            fout.write('M04 F{};\n'.format(F))
            fout.write('S{};\n'.format(S))
            fout.write('G00 X{0:.3f} Y{1:.3f};\n'.format(cx - L2, cy - L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx - L2, cy + L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx + L2, cy + L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx + L2, cy - L2))
            fout.write('G01 X{0:.3f} Y{1:.3f};\n'.format(cx - L2, cy - L2))
            fout.write('M05;\n')        # laser off
            if j == 0:
                fout.write('G4 P' + str(sleep * i) + '\n')  # 動作を指定時間止める
            fout.write('\n')

    # Finalize
    fout.write('S0;\n')
    fout.write('G00 X0.Y0.Z0.;\n')      # go back to zero
    fout.write('$32 = 0\n')     # Disable laser mode
    fout.write('M30;\n')        #program end
