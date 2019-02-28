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


def remove_new_line(list_):
    """
    """
    new_list = []
    
    for val in list_:
        new_list.append(val.strip())
    
    
    return new_list 

def flip_flags(str_):
    """
    """
    if str_ == 'T':
        new_str = 'F'
    elif str_ == 'F':
        new_str = 'T'
    
    return new_str

def distance_formula(x1, y1, z1, x2, y2, z2):
    
    diff_x = (float(x1) - float(x2))
    diff_y = (float(y1) - float(y2))
    diff_z = (float(z1) - float(z2))
    
    distance = math.sqrt(diff_x*diff_x + diff_y*diff_y + diff_z*diff_z)
    
    return distance


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designed 
                                     to parse VASP outcar files to provide 
                                     information on how each run converged.""")
    parser.add_argument('-i', action='store', dest='POSCAR_file', 
                        help='POSCAR file to be parsed to reveal structure info')
    parser.add_argument('-r', action='store', dest='Reciprocal', default=None,
                        help='Atom string to determine which atoms are frozen \
                        and which atoms are freeze to relax')
    parser.add_argument('-d', action='store', dest='DISTANCE', default=None,
                        help='Distance in A to determine frozen atoms')
    parser.add_argument('-w', action='store', dest='OUTPUT_SCF', default=False,
                        help='set as True to generate SCF convergence files')
    parser.add_argument('-e', action='store', dest='EDIT_ATOMS', default=None,
                        help='list of atoms to flip T or F flag in POSCAR')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')    
    args = parser.parse_args()
    
    try: 
        POSCAR = open(args.POSCAR_file,"r")
        MOD_POSCAR_STATUS = os.path.isfile(os.path.join(os.getcwd(), 'modified-POSCAR.txt'))
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the OUTCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
        
    if POSCAR != None and MOD_POSCAR_STATUS is False:
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
                edit_atoms = remove_new_line(edit_atoms)
            
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
                    MOD_POSCAR.write(' SKIP $$$ ' + POSCARlines[line])
                elif line == coordinate_line:
                    MOD_POSCAR.write(' SKIP $$$ ' + POSCARlines[line])
                elif line > coordinate_line:
                    atom     = str(atom_list[line].rjust(5) + ' $$$ ')
                    x_coords = str(POSCARlines[line].split()[0])
                    y_coords = str(POSCARlines[line].split()[1])
                    z_coords = str(POSCARlines[line].split()[2]) 
                    xcstr = str(x_coords).rjust(19)
                    ycstr = str(y_coords).rjust(20)
                    zcstr = str(z_coords).rjust(20)
                    
                    x_flags  = str(POSCARlines[line].split()[3])
                    y_flags  = str(POSCARlines[line].split()[4])
                    z_flags  = str(POSCARlines[line].split()[5])
                    if args.EDIT_ATOMS is not None: 
                        if atom_list[line] in edit_atoms:
                            x_flags = flip_flags(x_flags)
                            y_flags = flip_flags(y_flags)
                            z_flags = flip_flags(z_flags)
                    xfstr = str(x_flags).rjust(3)
                    yfstr = str(y_flags).rjust(3)
                    zfstr = str(z_flags).rjust(3)
                    MOD_POSCAR.write(atom +  xcstr +  ycstr + zcstr + xfstr + yfstr + zfstr + '\n')
            MOD_POSCAR.close()
    
    if args.Reciprocal != None and MOD_POSCAR_STATUS is True:
        if args.DISTANCE == None:
            print('\nYOU ARE MISSING THE -d FLAG TO SET THE DISTANCE CRITERA!!\n')
        elif args.DISTANCE != None: 
            re_central_atom = re.compile(str(args.Reciprocal))
            
            with open(os.path.join(os.getcwd(), 'modified-POSCAR.txt'), 'r') as MOD_POSCAR:
                MODPOSCARlines = MOD_POSCAR.readlines()
                MOD_POSCAR.close()
                
            # finding the coordinates to the atom that all other atoms will be 
            # compared to 
            for reline in range(0,len(MODPOSCARlines)-1):
                if re_central_atom.search(MODPOSCARlines[reline]):
                    x_coord_set = MODPOSCARlines[reline].split()[2]
                    y_coord_set = MODPOSCARlines[reline].split()[3]
                    z_coord_set = MODPOSCARlines[reline].split()[4]
            
            for mline in range(0,len(MODPOSCARlines)):
                if MODPOSCARlines[mline].split()[0] == 'SKIP':
                    if mline == 1:
                        SCALING_FACTOR = float(MODPOSCARlines[mline].split()[2])
                    elif mline == 2:
                        ax = float(MODPOSCARlines[mline].split()[2]) * SCALING_FACTOR
                        ay = float(MODPOSCARlines[mline].split()[3]) * SCALING_FACTOR
                        az = float(MODPOSCARlines[mline].split()[4]) * SCALING_FACTOR
                    elif mline == 3:
                        bx = float(MODPOSCARlines[mline].split()[2]) * SCALING_FACTOR
                        by = float(MODPOSCARlines[mline].split()[3]) * SCALING_FACTOR
                        bz = float(MODPOSCARlines[mline].split()[4]) * SCALING_FACTOR
                    elif mline == 4: 
                        cx = float(MODPOSCARlines[mline].split()[2]) * SCALING_FACTOR
                        cy = float(MODPOSCARlines[mline].split()[3]) * SCALING_FACTOR
                        cz = float(MODPOSCARlines[mline].split()[4]) * SCALING_FACTOR
                    elif mline == 5:
                        convert_M = np.array([[ax, ay, az], 
                                              [bx, by, bz],
                                              [cx, cy, cz]])
#                        convert_M = np.array([[ax, bx, cx],
#                                              [ay, by, cy],
#                                              [az, bz, cz]])
                        print(convert_M)
                else:
                    print(MODPOSCARlines[mline])
                    x_coord_frac = float(MODPOSCARlines[mline].split()[2])
                    y_coord_frac = float(MODPOSCARlines[mline].split()[3])
                    z_coord_frac = float(MODPOSCARlines[mline].split()[4])
                    
                    fractional_array = np.array([[x_coord_frac],
                                                 [y_coord_frac],
                                                 [z_coord_frac]])

                    print(np.dot(convert_M,fractional_array))
                    
                    distance = 0
#                    distance = distance_formula(x_coord_set, y_coord_set,
#                                                z_coord_set, x_coord_com,
#                                                y_coord_com, z_coord_com)
                    if distance > float(args.DISTANCE):
                        print('This attempt needs to be frozen')
                        print(distance, float(args.DISTANCE))
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
