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
#import sys
#import re 
import argparse
import ase 
from ase import io, build, Atoms


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
    parser.add_argument('-i', action='store', dest='INPUT_FILE', default=None,
                        help='file to read')
    parser.add_argument('-t', action='store', dest='TYPE_FILE', default="vasp",
                        help='type of file for input (vasp, cif, etc.)')
    args = parser.parse_args()
     
    
    
    structure = ase.Atoms(ase.io.read(args.INPUT_FILE, format=args.TYPE_FILE))
    
    print(structure.pbc)
    print(structure.get_cell)
    print(structure.set_scaled_positions)
    
    
       
    ase.io.write('testing.cif',structure,format=args.TYPE_FILE)

    
             
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
