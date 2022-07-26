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
#print(sys.argv)
elems = []
for arg in range(1,len(sys.argv)-1):
    elem = sys.argv[arg].lower().capitalize()
    if os.path.isfile('/zfs/curium/VASP/PPs/120423/PBE/'+elem+'/POTCAR'):
        elems.append(elem)
#print(elems)    
with open('POTCAR', 'w+') as outPOTCAR:
    for elem in elems:
        print ('Adding POTCAR for '+elem)
        with open('/zfs/curium/VASP/PPs/120423/PBE/'+elem+'/POTCAR') as inPOTCAR:
            outPOTCAR.write(inPOTCAR.read())

if os.path.isfile('POTCAR'):
    print (subprocess.Popen('grep PAW POTCAR', shell=True, stdout=subprocess.PIPE).stdout.read())
