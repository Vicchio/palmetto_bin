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
from ase import Atoms
from ase.io import read, write
from ase.build import sort 

filename=sys.argv[1].split('.')[0]

structure = read(sys.argv[1], format='cif')
sorted_structure = sort(structure)
write(filename + '.POSCAR',sorted_structure,format='vasp')

# To create for ASE not including the list of atoms after line 5... 

f = open(filename + '.POSCAR','r')
contents = f.readlines()
f.close

contents.insert(5, contents[0])

f = open(filename + '.POSCAR','w')
contents = "".join(contents)
f.write(contents)
f.close()


