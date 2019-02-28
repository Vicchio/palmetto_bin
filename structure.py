#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-02-27
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# [structure.py] Provides information on the POSCAR to identify which flags
# should be frozen. T  

#
# Note: This script is a modified version of a script (grad2.py) written by 
# Peter Larsson. The original can be found at: 
# https://www.nsc.liu.se/~pla/vasptools/. 
#
# Peter Larsson constructed the orginal script (AS MENTIONED ABOVE). I needed 
# the script to perform similar operations, and I noticed a small error in his
# orginal script that I wanted to correct. I DO NOT take credit for the
# algorithms generated here.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: POSCAR from VASP 
# OUTPUT: txt file similar to VASP POSCAR except contains atom name 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# L I S T   O F   I M P O R T S 
import subprocess 
import os 
import sys
import math
import numpy as np 
import re 
import argparse
import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designed 
                                     to parse VASP outcar files to provide 
                                     information on how each run converged.""")
    parser.add_argument('-i', action='store', dest='POSCAR_file', 
                        help='POSCAR file to be parsed to reveal structure info')
    parser.add_argument('-w', action='store', dest='OUTPUT_SCF', default=False,
                        help='set as True to generate SCF convergence files')
    parser.add_argument('-e', action='store', dest='EDIT_ATOMS', default=None,
                        help='list of atoms to flip T or F flag in POSCAR')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')    
    args = parser.parse_args()
    
    try: 
        POSCAR = open(args.POSCAR_file,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the OUTCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
        
    if POSCAR != None:
        print('\nThere exists an POSCAR file!\n')
        POSCARfile = args.POSCAR_file
        POSCARlines = POSCAR.readlines()
        
        SEARCH_='Direct'
        
        
        
        atoms_dict = {}
        
        coordinate_line = int(str(subprocess.check_output(['grep', '-n', SEARCH_, POSCARfile])).split('\'')[1].split(':')[0])
                
        with open(os.path.join(os.getcwd(), 'modified-POSCAR.txt'), 'w') as MOD_POSCAR:        
            for line in range(0,len(POSCARlines)-1):
                if line <= coordinate_line - 1:
                    if line == 5:
                        for atom in POSCARlines[line].split():
                            atoms_dict[atom] = None
                    elif line == 6:
                        atom_keys = atom_dict.keys()
                        for i in atom_keys:
                            atoms_dict[atom_keys][i] = POSCARlines[line].split()[i]
                
                    print(atoms_dict)
                elif line > coordinate_line - 1:
                    x_coords = float(POSCARlines[line].split()[0])
                    y_coords = float(POSCARlines[line].split()[1])
                    z_coords = float(POSCARlines[line].split()[2])                    
                    x_flags  = str(POSCARlines[line].split()[3])
                    y_flags  = str(POSCARlines[line].split()[4])
                    y_flags  = str(POSCARlines[line].split()[5])
  
                    
                    
                    if args.EDIT_ATOMS is not None:
                        print('Edit Atoms is not none.')
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
