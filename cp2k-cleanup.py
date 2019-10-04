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
        
        line_count = 1
        for line in inputlines:
            
            if re_SUBSYS.search(line):
                print(line)
                print(line_count)
                
            if re_SUBSYSEND.search(line):
                print(line)
                print(line_count)
                
            if re_CELL.search(line):
                print(line)
                print(line_count)
                            
            if re_CELLEND.search(line):
                print(line)
                print(line_count)
                
            if re_COORD.search(line):
                print(line)
                print(line_count)
                COORD_COUNT_STATUS = True
                print(COORD_COUNT_STATUS)
                print(COORD_FINISH_STATUS)
            
            if COORD_COUNT_STATUS == True:
                print('I MADE IT HERE')
                if COORD_COUNT_STATUS == False: 
                    print('I MADE IT HERE')
                    print(line)

            if re_COORDEND.search(line):
                print(line)        
                print(line_count)                
                COORD_FINISH_STATUS = True
            

            line_count += 1
                
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
