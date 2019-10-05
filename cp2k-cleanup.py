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
        
        
    with open(args.INPUT_FILE, 'r') as input_file:
        inputlines = input_file 
        
        # defining the search parameters for the OUTCAR file
        re_SUBSYS     = re.compile('&SUBSYS')
        re_SUBSYSEND  = re.compile('&END SUBSYS')
        re_CELL       = re.compile('&CELL')
        re_CELLEND    = re.compile('&END CELL')
        re_COORD      = re.compile('&COORD')
        re_COORDEND   = re.compile('&END COORD')
        
        # defining key parameters 
        INPUT_FINISH_STATUS = False
        COORD_FINISH_STATUS = False
        COORD_COUNT_STATUS  = False
        print_string = None 
        atom_dict = {}
        line_count = 1
        atom_total_count = 0 
        
        for line in inputlines:
            
            if re_SUBSYS.search(line):
                print_string = line
                
            if re_SUBSYSEND.search(line):
                print_string = line
                
            if re_CELL.search(line):
                print_string = line
                            
            if re_CELLEND.search(line):
                print_string = line
                
            if re_COORD.search(line):
                print_string = line
                COORD_COUNT_STATUS = True
                
            if re_COORDEND.search(line):
                print_string = line              
                COORD_FINISH_STATUS = True
        
            if COORD_FINISH_STATUS == False and COORD_COUNT_STATUS == True:
                line_info = line.split()
                if len(line_info) == 4:
                    if line_info[0] not in atom_dict.keys():
                        atom_dict[str(line_info[0])] = 0 
                    atom_dict[str(line_info[0])] += 1 
                    print_string = (str(line_info[0]).rjust(9) + 
                                    str(line_info[1]).rjust(27) + 
                                    str(line_info[2]).rjust(27) + 
                                    str(line_info[3]).rjust(27) + 
                                    (str('# ') + str(line_info[0]) + 
                                    str(atom_total_count + 1).zfill(3)).rjust(9) + 
                                    (str('VMD') + str(atom_total_count).zfill(3)).rjust(7))
                    atom_total_count += 1

            line_count += 1
            if print_string is not None: 
                print(print_string)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
