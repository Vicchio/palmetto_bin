#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-01-14
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Turns on selective dynamics in POSCAR file  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: POSCAR file 
# OUTPUT: POSCAR file that includes selective dynamics  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os

def main():
	filepath = sys.argv[1]
		
	if not os.path.isfile(filepath):
		print("File path {} does not exist. Exiting...".format(filepath))
		sys.exit()	

	with open(filepath) as f:
		cnt = 0 
		for line in f:
			if cnt == 0:
				create_atom_counts(line)
			cnt += 1 

def create_atom_counts(line_atoms):
	list_atoms = line_atoms.split()
	
	print(list_atoms)
	return 

#f = open(org_file, 'r')

#for line in f: 
#	print(f)

#print(f.readlines())

if __name__ == '__main__':
	main()


