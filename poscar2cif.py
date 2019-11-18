#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-04-24
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Converts VASP POSCAR to .cif files  using the ASE library 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: POSCAR
# OUTPUT: cif 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os
from ase import Atoms
from ase.io import read, write
from ase.build import sort 

filename=sys.argv[1]

print(filename)


structure = read(filename, format='vasp')
sorted_structure = sort(structure)
write(filename + '.cif',sorted_structure,format='cif')

# To create for ASE not including the list of atoms after line 5... 

#f = open(filename + '.POSCAR','r')
#contents = f.readlines()
#f.close

#contents.insert(5, contents[0])

#f = open(filename + '.POSCAR','w')
#contents = "".join(contents)
#f.write(contents)
#f.close()


