#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-10-28
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Extracts the xyz coordinates for the optimized structure 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: requires a .xyz and a .inp file to generate the perioduc information 
#  INPUT: optional inputs also include how the periodic structure should be 
#         be duplicated
# OUTPUT: .xyz file containing the periodic information of the cluster 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os
import argparse 
import re
import subprocess 
import shutil

DIR_ = os.getcwd()
FAIL = '\033[91m'
ENDC = '\033[0m'


# Parsing the command line arguments
parser = argparse.ArgumentParser(description="""\n
                    This script is designed to extract the CP2K output
                    coordinates from a previous optimization and label 
                    those coordinates.\n""")
parser.add_argument('-i', action='store', dest='INP_FILE', 
                    default=None, help='inp file from CP2K')
parser.add_argument('-x', action='store', dest='XYZ_FILE',
                    default=None, help='xyz coordinate information')
parser.add_argument('-t', action='store', dest='MODE_parameter',
                    default='1 1 2', help='how to manipulate the unit cell')
parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
args = parser.parse_args()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():

    if os.path.isfile(args.INP_FILE) is True:
        INPFILE = args.INP_FILE
    try:
        inpfile = open(INPFILE,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the .inp file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
    
    if os.path.isfile(args.XYZ_FILE) is True:
        XYZFILE = args.XYZ_FILE
    try:
        xyzfile = open(XYZFILE,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the .xyz file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
    
        
    with open(args.INP_FILE,"r") as inp_file, \
    open(args.XYZ_FILE, "r") as xyz_file, \
    open(os.path.join(DIR_, args.XYZ_FILE.split('.')[0] + '-periodic.xyz'), 'w') as PER_FILE:
        xyz_lines = xyz_file
        inp_lines = inp_file
        
        # defining the search parameters for the inp_file 
        re_NUMATOMS   = re.compile('NUMBER_OF_ATOMS')
        re_CELL       = re.compile('&CELL')
        re_CELLEND    = re.compile('&END CELL')
        re_ACELL      = re.compile(' A ')
        re_BCELL      = re.compile(' B ')
        re_CCELL      = re.compile(' C ')
        
        for line in inp_lines:
            
            if re_NUMATOMS.search(line):
                inp_number_atoms = line.split()[1]
                
            if re_CELL.search(line):
                CELL_STATUS = True 

            if re_CELLEND.search(line):
                CELL_STATUS = False
                
            if re_ACELL.search(line) and CELL_STATUS == True:
                inp_a_cell = line.split()

            if re_BCELL.search(line) and CELL_STATUS == True:
                inp_b_cell = line.split()

            if re_CCELL.search(line) and CELL_STATUS == True:
                inp_c_cell = line.split()
                
                
        inp_file.close()
        
        
        manipulation = args.MODE_parameter
        x_manipulation = False
        y_manipulation = False
        z_manipulation = False
        
        if int(manipulation.split()[0]) != 1: 
            x_manipulation = True
            
        if int(manipulation.split()[1]) != 1: 
            y_manipulation = True

        if int(manipulation.split()[2]) != 1: 
            z_manipulation = True
            z_coord_man = float(inp_c_cell[3])
            
            
        coordinate_change = -2 
        for i in args.MODE_parameter.split(): 
            coordinate_change += int(i)  
        
        for line in xyz_lines: 
            if len(line.split()) == 4 or len(line.split()) == 5: 
                x_coord = float(line.split()[1])
                y_coord = float(line.split()[2])
                z_coord = float(line.split()[3])
                PER_FILE.write(line)
                
                if x_manipulation is True: 
                    pass
                if y_manipulation is True: 
                    pass
                if z_manipulation is True: 
                    z_coord_new = z_coord + z_coord_man
                    
                    print_string = (str(line.split()[0]).rjust(9) + 
                                    str(line.split()[1]).rjust(27) + 
                                    str(line.split()[2]).rjust(27) + 
                                    str(str(z_coord_new).rjust(27)) + '\n') 
                    PER_FILE.write(print_string)
            elif len(line.split()) == 1: 
                new_number_atoms = (int(line))*coordinate_change
                print_string = (str(new_number_atoms).rjust(14))    
                PER_FILE.write(print_string + '\n')
                
            else:
                PER_FILE.write(line)
       
        PER_FILE.close()
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
