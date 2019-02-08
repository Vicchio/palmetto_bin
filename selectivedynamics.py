#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-01-25
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Converts POSCAR file with Direct setups to Selective Dynamics
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: POSCAR file that has Direct
# OUTPUT: POSCAR file that has Selective dynamics enabled  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os
from itertools import groupby
import numpy as np

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def main():
	temp_file = 'POSCAR-direct'
	read_file = sys.argv[1]

	with open(read_file, 'r') as f_read, open(temp_file, 'w') as f_temp:
		cnt = 1 # the count corresponds to the file number in vim
		for line in f_read:
			if cnt > 8:
				write_line = change_to_selective(line)
			elif cnt == 8:
				f_temp.write('Selective Dynamics\n')
				write_line = line
			elif cnt <= 7:
				write_line = line
			f_temp.write(write_line)
			cnt += 1
	f_read.close()
	f_temp.close()
	os.rename(read_file, read_file + '-noselective')
	os.rename(temp_file, read_file)
	

def change_to_selective(line):
	list = ['  ']
	list.extend(line.split())
	list.append(' F   F   F\n')
	new_line = "  ".join(list)
	return new_line


if __name__ == '__main__':
	main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

