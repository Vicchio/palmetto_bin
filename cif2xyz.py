#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2020-11-12
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Converts .cif files into XYZ files using the ASE library 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: CIF filename (note that data_ must be the first 5 characters)
# OUTPUT: XYZ file 
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
write(filename + '.xyz',sorted_structure,format='xyz')

