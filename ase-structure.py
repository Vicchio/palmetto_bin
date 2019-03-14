#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-03-13
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# [ase-structure.py] Converts the structuce using ASE tools   
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# L I S T   O F   I M P O R T S 

import os 
import sys
import re 
import argparse
import ase

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'
DIR_ = os.getcwd()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""HI""")
    parser.add_argument('-i', action='store', dest='POSCAR_FILE', default=None,
                        help='POSCAR file to read')
    parser.add_argument('-p', action='store', dest='POTCAR_FILE', default=None,
                        help='POTCAR file to read')
    args = parser.parse_args()
    
    
                
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
