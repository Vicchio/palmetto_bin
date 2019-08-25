#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-01-14
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Converts .cif files into VASP POSCAR files using the ASE library 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: CIF filename (note that data_ must be the first 5 characters)
# OUTPUT: POSCAR file containing the same information as in the CIF 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os
import argparse 
from ase import Atoms
from ase.io import read, write
from ase.build import sort 


# Parsing the command line arguments
parser = argparse.ArgumentParser(description="""\n
                    This script is designed to parser a CP2K output file 
                    to check for convergence. The script will determine how
                    the calculation performed.\n""")
parser.add_argument('-i', action='store', dest='INPUT_FILE', 
                    default=None, help='input file to parse')
parser.add_argument('-e', action='store', dest='INPUT_FILE_TYPE', 
                    default=None, help='input file to parse')
parser.add_argument('-o', action='store', dest='OUTPUT_FILE',
                    default=None, help='extension for the output file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
args = parser.parse_args()


filename=args.INPUT_FILE.split('.')[0]
structure = read(args.INPUT_FILE,format=args.INPUT_FILE_TYPE)
sorted_structure = sort(structure)
write(filename + args.OUTPUT_FILE,sorted_structure,format=args.OUTPUT_FILE)

# To create for ASE not including the list of atoms after line 5... 

#f = open(filename + '.POSCAR','r')
#contents = f.readlines()
#f.close
#
#contents.insert(5, contents[0])
#
#f = open(filename + '.POSCAR','w')
#contents = "".join(contents)
#f.write(contents)
#f.close()
#
#
