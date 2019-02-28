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

def list_of_atoms(top_buffer,dict_):
    """
    INPUT the buffer number of lines at the top of the POSCAR file and a 
    dictionary containing keys as atoms and values as the number of those atoms
    in the system. The OUTPUT is a list containing the order of the atoms in 
    your system to help determine what atoms should be frozen and which should 
    be allowed to relax. 
    
    [Inputs]
    (1) top_buffer - the number of lines before the coordinates begin in POSCAR
    (2) dict_      - dictionary containing the information about system atoms
    
    [Outputs]
    (1) list_of_atoms - list containing all the atoms in the system (IN ORDER)
    """
    
    list_of_atoms = []
    
    for x in range(0,top_buffer+1):
        list_of_atoms.append('SKIP')
    
    for key, val in dict_.items():
        for j in range(1,val+1):
            list_of_atoms.append(str(key)+str(j).zfill(3))
    
    return list_of_atoms

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
        POSCAR.close()
        
        
        
        SEARCH_='Direct'
        
        atoms_dict = {}
        
        coordinate_line = int(str(subprocess.check_output(['grep', '-n', SEARCH_, POSCARfile])).split('\'')[1].split(':')[0])-1
                
        with open(os.path.join(os.getcwd(), 'modified-POSCAR.txt'), 'w') as MOD_POSCAR:
            if args.EDIT_ATOMS is not None: 
                with open(os.path.join(os.getcwd(), args.EDIT_ATOMS), 'r') as EDIT_ATOMS:
                    edit_atoms = EDIT_ATOMS.readlines()
                    EDIT_ATOMS.close()
            
            print(len(POSCARlines))
            for line in range(0,len(POSCARlines)-1):
                if line < coordinate_line:
                    if line == 5:
                        for atom in POSCARlines[line].split():
                            atoms_dict[atom] = None
                    elif line == 6:
                        atom_keys = atoms_dict.keys()
                        count = 0 
                        for atom_add in atom_keys:
                            atoms_dict[atom_add] = int(POSCARlines[line].split()[count])
                            count += 1  
                        atom_list = list_of_atoms(coordinate_line, atoms_dict)
                    MOD_POSCAR.write('SKIP $$$ ' + POSCARlines[line])
                elif line == coordinate_line:
                    MOD_POSCAR.write('SKIP $$$ ' + POSCARlines[line])
                elif line > coordinate_line:
#                    print(POSCARlines[line])
                    atom     = str(atom_list[line] + ' $$$ ').rjust(8)
#                    print(atom)
                    x_coords = float(POSCARlines[line].split()[0])
                    y_coords = str(POSCARlines[line].split()[1])
                    z_coords = str(POSCARlines[line].split()[2])              
                    x_flags  = str(POSCARlines[line].split()[3])
                    y_flags  = str(POSCARlines[line].split()[4])
                    z_flags  = str(POSCARlines[line].split()[5])

                    if args.EDIT_ATOMS is None:
                        xcstr = str(x_coords).rjust(20)
                        ycstr = str(y_coords).rjust(19)
                        zcstr = str(z_coords).rjust(19)
#                        print(xcstr, ycstr, zcstr)
                        MOD_POSCAR.write(atom +  xcstr +  ycstr + zcstr + '\n')
                    elif args.EDIT_ATOMS is not None: 
                        if atom_list[line] in edit_atoms:
                            print('WE FOUND A MATCH')

        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
