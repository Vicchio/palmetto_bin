#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-10-04
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Extracts the xyz coordinates for the optimized structure 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: either the trajectory or the restart file
# OUTPUT: POSCAR file containing the same information as in the CIF 
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
parser.add_argument('-i', action='store', dest='INPUT_FILE', 
                    default=None, help='input file to parse')
parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
args = parser.parse_args()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():

    if os.path.isfile(args.INPUT_FILE) is True:
        INPUTFILE = args.INPUT_FILE
    try:
        inputfile = open(INPUTFILE,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the OUTCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
        
        
    with open(args.INPUT_FILE, 'r') as input_file, \
    open(os.path.join(DIR_, args.INPUT_FILE + '-clean'), 'w') as CLEAN_INPUT, \
    open(os.path.join(DIR_, args.INPUT_FILE + '-xyz'), 'w') as XYZ_FILE:
        inputlines = input_file 
        
        # defining the search parameters for the OUTCAR file
        re_SUBSYS     = re.compile('&SUBSYS')
        re_SUBSYSEND  = re.compile('&END SUBSYS')
        re_CELL       = re.compile('&CELL')
        re_CELLEND    = re.compile('&END CELL')
        re_NUMATOMS   = re.compile('NUMBER_OF_ATOMS')
        re_COORD      = re.compile('&COORD')
        re_COORDEND   = re.compile('&END COORD')
        re_POTEN      = re.compile('&POTENTIAL')
        re_POTENEND   = re.compile('&END POTENTIAL')
        re_KINDEND    = re.compile('&END KIND')
        
        
        # defining key parameters 
        INPUT_FINISH_STATUS = False
        COORD_FINISH_STATUS = False
        COORD_COUNT_STATUS  = False
        print_string_status = True
        print_string = None 
        print_xyz = None
        atom_dict = {}
        line_count = 1
        atom_total_count = 0 
        
        for line in inputlines:
            print_string = line.strip('\n')
            
            if re_SUBSYS.search(line):
                print_string = line.strip('\n')
                
            if re_SUBSYSEND.search(line):
                print_string = line.strip('\n')
                
            if re_CELL.search(line):
                print_string = line.strip('\n')
                            
            if re_CELLEND.search(line):
                print_string = line.strip('\n')
                
            if re_NUMATOMS.search(line):
                NUMBER_OF_ATOMS_SYS = line.split()[1]
                
            if re_COORD.search(line):
                print_string = line.strip('\n')
                COORD_COUNT_STATUS = True
                print_xyz = '      NUM_ATOMS_SYSTEM \n i =        1, E =     -0000.000000000'
                
            if re_COORDEND.search(line):
                print_string = line.strip('\n')              
                COORD_FINISH_STATUS = True
                print_xyz = None
        
            if COORD_FINISH_STATUS == False and COORD_COUNT_STATUS == True:
                line_info = line.split()
                if len(line_info) == 4:
                    if line_info[0] not in atom_dict.keys():
                        atom_dict[str(line_info[0])] = 0 
                    atom_dict[str(line_info[0])] += 1 
                    print_string = None
                    print_string = (str(line_info[0]).rjust(9) + 
                                    str(line_info[1]).rjust(27) + 
                                    str(line_info[2]).rjust(27) + 
                                    str(line_info[3]).rjust(27) + 
                                    (str('  #VMD') + str(atom_total_count).zfill(3)).rjust(7) +
                                    str(line_info[0].strip()) + 
                                    str(atom_total_count + 1).zfill(3))
                    
                    print_xyz = print_string
                    atom_total_count += 1
            
            if re_POTEN.search(line):
                print_string_status = False
            
            if re_POTENEND.search(line):
                print_string_status = False 
                
            if re_KINDEND.search(line):
                print_string_status = True
                
            line_count += 1
            if print_xyz is not None: 
                XYZ_FILE.write(print_xyz + '\n')
                print(print_xyz)
                print_xyz = None
            if print_string is not None and print_string_status is True: 
                CLEAN_INPUT.write(str(print_string) + '\n')
    
    
    XYZ_FILE.close()
    sed_cmd = 's/NUM_ATOMS_SYSTEM/' + str('     ') + str(NUMBER_OF_ATOMS_SYS) + '/g'
    subprocess.call(['sed', '-i', sed_cmd, os.path.join(DIR_, args.INPUT_FILE + '-xyz')])
    
    shutil.move(os.path.join(os.getcwd(), args.INPUT_FILE + '-xyz'), os.path.join(os.path.join(os.getcwd()), args.INPUT_FILE.split('.')[0] + '.xyz'))
    shutil.move(os.path.join(os.getcwd(), args.INPUT_FILE), os.path.join(os.path.join(os.getcwd()), args.INPUT_FILE.split('.')[0] + '.inp-raw'))
    shutil.move(os.path.join(os.getcwd(), args.INPUT_FILE + '-clean'), os.path.join(os.path.join(os.getcwd()), args.INPUT_FILE.split('.')[0] + '.inp'))
    
    #TODO: change the NUM_ATOMS_SYSTEM to then correct the xyz-file 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
