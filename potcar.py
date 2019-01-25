#!/usr/bin/env python

#####
#
# USAGE: In VASP job directory: potcar.py elem1 elem2...
#
# All "elem#" values are the appropriate 1- or 2-letter element symbols.
#
#####

import os
import sys
import subprocess

if os.path.isfile('POTCAR'):
    os.remove('POTCAR')

elems = []
for arg in range(1,len(sys.argv)):
    elem = sys.argv[arg].lower().capitalize()
#    if os.path.isfile('/common/curium/VASP/PPs/120423/PBE/'+elem+'/POTCAR'):
    if os.path.isfile('/common/curium/VASP/170517_PPs/potpaw_PBE/'+elem+'/POTCAR'):
        elems.append(elem)
    else:
        print('Incorrect element symbol: '+elem)
        sys.exit(1)
    
with open('POTCAR', 'w+') as outPOTCAR:
    for elem in elems:
#        print('Adding POTCAR for '+elem)
#        with open('/common/curium/VASP/PPs/120423/PBE/'+elem+'/POTCAR') as inPOTCAR:
        with open('/common/curium/VASP/170517_PPs/potpaw_PBE/'+elem+'/POTCAR') as inPOTCAR:
            outPOTCAR.write(inPOTCAR.read())

'''
if os.path.isfile('POTCAR'):
    stdoutdata = subprocess.run(['grep','PAW','POTCAR'], stdout=subprocess.PIPE)
    print(stdoutdata.stdout.decode('utf-8'))
'''

sys.exit(0)
